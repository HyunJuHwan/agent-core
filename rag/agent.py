from rag.qdrant_client import QdrantHandler
from rag.vector_search import VectorSearch
from rag.conversation_manager import ConversationManager
from planner.planner import get_tool_plan
from executor.executor import execute_tool
from validator.validator import validate_call
from utils.alias_map import AliasMapper
from context.store import context_store
import logging

alias_mapper = AliasMapper()

class AgentCore:
    def __init__(self, collection_name="search_history"):
        # Qdrant 핸들러 초기화
        self.qdrant_handler = QdrantHandler()
        
        # `search_history`와 `user_profiles` 컬렉션 생성
        # self.qdrant_handler.create_collection("search_history")
        
        # VectorSearch 인스턴스 초기화
        self.vector_search = VectorSearch(collection_name)
        self.conversation_manager = None

    async def generate_response(self, user_query, user_id):
        """LLM을 사용하여 답변을 생성하고, 이전 히스토리를 반영합니다."""
        # 사용자별로 ConversationManager 초기화
        self.conversation_manager = ConversationManager(user_id)

        # 사용자 프롬프트 저장
        # self.conversation_manager.add_user_prompt(user_query)

        # Qdrant에서 유사한 질문 히스토리 검색
        similar_history = self.vector_search.search_similar_history(user_query, user_id)

        # 유사한 질문과 답변을 문맥으로 추가
        context_for_llm = ""
        if similar_history:
            context_for_llm = " ".join([f"Question: {entry['question']} Answer: {entry['answer']}" for entry in similar_history])
        else:
            context_for_llm = "No previous history found."

        # LLM에 문맥과 새로운 질문을 합쳐서 전달
        context_for_llm += f" Now, the user is asking: {user_query}"

        print(f"context_for_llm: {context_for_llm}")

        # 도구 호출 계획 생성 (기존 로직 사용)
        tool_calls = await get_tool_plan(context_for_llm)
        logging.info(f"Tool calls: {tool_calls}")

        # 도구 호출 계획 저장
        # self.conversation_manager.add_tool_plan(tool_calls)

        results = []
        for call in tool_calls:
            if not validate_call(call):
                return {"error": f"Validation failed for tool: {call.tool}"}
            
            # 공통 ID 매핑 처리
            if "character_ids" in call.input:
                call.input["character_ids"] = alias_mapper.resolve(call.input["character_ids"])
            if "scene_ids" in call.input:
                call.input["scene_ids"] = alias_mapper.resolve(call.input["scene_ids"])
            
            result = await execute_tool(call)
            results.append(result.model_dump())

            out = result.output
            if "character_id" in out:
                alias_mapper.register(call.tool, out["character_id"])
            if "scene_id" in out:
                alias_mapper.register(call.tool, out["scene_id"])

            # 대화 흐름에 저장
            # self.conversation_manager.add_tool_result(result)

            # 최신 도구 실행 결과 별도로 저장
            context_store.save_result(call.tool, result)

        # Qdrant에 질문, LLM 응답, MCP 응답 저장
        self.qdrant_handler.upsert_data(
            self.vector_search.collection_name,
            [
                {
                    "text": user_query,  # 질문
                    "llm_answer": tool_calls,  # LLM 응답
                    "mcp_answer": results,  # MCP 응답
                    "user_id": user_id
                }
            ]
        )

        return {"result": results}
