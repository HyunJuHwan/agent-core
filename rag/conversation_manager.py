# rag/conversation_manager.py
from rag.qdrant_client import QdrantHandler

class ConversationManager:
    def __init__(self, user_id, qdrant_handler=None):
        self.user_id = user_id
        self.user_prompts = []
        self.tool_plans = []
        self.tool_results = []
        self.qdrant_handler = qdrant_handler or QdrantHandler()  # Qdrant 핸들러 초기화

    def add_user_prompt(self, prompt):
        """사용자의 프롬프트를 저장합니다."""
        self.user_prompts.append(prompt)
        # 프롬프트를 벡터화하여 Qdrant에 저장
        self.qdrant_handler.upsert_data("search_history", [{"text": prompt, "user_id": self.user_id}])

    def add_tool_plan(self, tool_calls):
        """도구 호출 계획을 저장합니다."""
        self.tool_plans.append(tool_calls)

    def add_tool_result(self, result):
        """도구 실행 결과를 저장합니다."""
        self.tool_results.append(result)
        # 결과를 벡터화하여 Qdrant에 저장 (필요한 경우)
        # 예시로 tool_results를 Qdrant에 저장하는 코드 추가 가능
        self.qdrant_handler.upsert_data("search_history", [{"text": result.output, "user_id": self.user_id}])
