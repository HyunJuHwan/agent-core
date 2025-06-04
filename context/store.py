import redis
import json
from config import settings
from fastapi.encoders import jsonable_encoder
from utils.patch import patch_output_urls

r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)

class RedisContextStore:
    def save_result(self, key: str, result: object):
        if hasattr(result, "model_dump"):
            result = result.model_dump()

        result = patch_output_urls(result.get("output", {}))
        wrapped = {
            "tool": key,
            "output": result
        }

        encoded = json.dumps(jsonable_encoder(wrapped))
        r.set(f"context:{key}", encoded, ex=3600)

    def get_result(self, key: str):
        data = r.get(f"context:{key}")
        return json.loads(data) if data else None

    def save_conversation(self, user_id: str, messages: list[dict]):
        r.set(f"conv:{user_id}", json.dumps(messages, ensure_ascii=False), ex=3600)

    def get_conversation(self, user_id: str) -> list[dict]:
        data = r.get(f"conv:{user_id}")
        return json.loads(data) if data else []

    def append_to_conversation(self, user_id: str, new_entries: list[dict]):
        messages = self.get_conversation(user_id)
        messages.extend(new_entries)
        self.save_conversation(user_id, messages[-20:])  # 최근 20개만 유지

context_store = RedisContextStore()
