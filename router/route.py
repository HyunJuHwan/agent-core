from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import FileResponse
from planner.planner import get_tool_plan
from executor.executor import execute_tool
from validator.validator import validate_call
from utils.alias_map import AliasMapper
from context.store import context_store
from context.context import ConversationManager
from pathlib import Path
from rag.agent import AgentCore
import logging

logging.basicConfig(level=logging.INFO)
alias_mapper = AliasMapper()
router = APIRouter()

@router.post("/route")
async def route_agent(request: Request):
    body = await request.json()
    prompt = body.get("prompt")
    user_id = body.get("user_id") or "1"
    if not prompt:
        return {"error": "prompt is required"}

    agent = AgentCore()
    results = await agent.generate_response(prompt, user_id)

    # # ConversationManager 초기화
    # conversation_manager = ConversationManager(user_id)

    # # 사용자 프롬프트 저장
    # conversation_manager.add_user_prompt(prompt)

    # # 도구 호출 계획 생성
    # tool_calls = await get_tool_plan(prompt)
    # logging.info(f"Tool calls: {tool_calls}")

    # # 도구 호출 계획 저장
    # conversation_manager.add_tool_plan(tool_calls)

    # results = []
    # for call in tool_calls:
    #     if not validate_call(call):
    #         return {"error": f"Validation failed for tool: {call.tool}"}
        
    #      # 공통 ID 매핑 처리
    #     if "character_ids" in call.input:
    #         call.input["character_ids"] = alias_mapper.resolve(call.input["character_ids"])
    #     if "scene_ids" in call.input:
    #         call.input["scene_ids"] = alias_mapper.resolve(call.input["scene_ids"])
    #     # buildWebtoon만 별도로 speech_bubbles 처리
    #     if call.tool == "buildWebtoon" and "speech_bubbles" in call.input:
    #         call.input["speech_bubbles"] = alias_mapper.resolve_scene_bubbles(call.input["speech_bubbles"])

    #     result = await execute_tool(call)
    #     results.append(result.model_dump())

    #     out = result.output
    #     if "character_id" in out:
    #         alias_mapper.register(call.tool, out["character_id"])
    #     if "scene_id" in out:
    #         alias_mapper.register(call.tool, out["scene_id"])

    #     # 대화 흐름에 저장
    #     conversation_manager.add_tool_result(result)
    #     # 최신 도구 실행 결과 별도로 저장
    #     context_store.save_result(call.tool, result)

    return {"result": results}

STATIC_BASE_DIR = Path("/Users/soulx/Desktop/workspace/scenario-word/dist/tools")
ALLOWED_DIRS = {"character", "scene", "video", "webtoon"}

@router.get("/image/{type}/{filename}")
async def get_image(type: str, filename: str):
    if type not in ALLOWED_DIRS:
        raise HTTPException(status_code=400, detail="Invalid image category")

    full_path = STATIC_BASE_DIR / type / filename

    if not full_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(path=full_path)
