from fastapi import HTTPException
from schemas.tool_call import ToolCall
from schemas.llm_request import LLMRequest
from planner.prompt_builder import build_prompt
from config import settings
import httpx
import json
import logging
import re

logging.basicConfig(level=logging.INFO)

async def get_tool_plan(user_prompt: str) -> list[ToolCall]:
    system, prompt = build_prompt(user_prompt)
    payload = LLMRequest(model="gemma-3-4b", system=system, prompt=prompt, stream=False)
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            res = await client.post(settings.LLM_URL, json=payload.model_dump())
        except httpx.RequestError as e:
            logging.error(f"🔌 LLM 서버 연결 실패: {e}")
            raise HTTPException(status_code=503, detail="LLM 서버에 연결할 수 없습니다.")
    raw = res.json().get("response", "[]")
    parsed = extract_json(raw)
    if not parsed:
        raise ValueError("LLM 응답이 비어있거나 유효하지 않음")
    try:
        logging.info(f"LLM 응답: {raw}")
        plan_list = json.loads(parsed)
    except json.JSONDecodeError as e:
        raise ValueError(f"LLM 응답이 유효한 JSON 배열이 아님: {e}")

    return [ToolCall.model_validate(call) for call in plan_list]

def extract_json(text: str) -> str:
    cleaned = re.sub(r"^```json\\s*|^json\\s*", "", text.strip(), flags=re.IGNORECASE)
    cleaned = re.sub(r"^```[^\n]*\n|```$", "", cleaned.strip())
    return cleaned.strip()