from schemas.tool_call import ToolCall, ToolResult
from fastapi import HTTPException
from config import settings
from utils.patch import patch_output_urls
import httpx
import logging
import json

_mcp_session_id: str | None = None

def get_mcp_session_id() -> str:
    if not _mcp_session_id:
        raise RuntimeError("❌ MCP 세션이 초기화되지 않았거나 세션 ID가 없습니다.")
    return _mcp_session_id

async def execute_tool(call: ToolCall) -> ToolResult:
    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            res = await client.post(settings.MCP_URL, json={
                "jsonrpc": "2.0",
                "id": "call-001",
                "method": "tools/call",
                "params": {
                    "name": call.tool,
                    "arguments": call.input
                }
            }, headers={
                "Accept": "application/json, text/event-stream",
                "Content-Type": "application/json",
                "Mcp-Session-Id": get_mcp_session_id()
            })

            raw = res.json()
            print(f"🔌 MCP 응답: {raw}")
            output_text = raw[0]["result"]["content"][0]["text"]
            parsed_output = json.loads(output_text)
            patched_output = patch_output_urls(parsed_output)
        except httpx.ReadTimeout:
            logging.error("🕒 MCP 응답 타임아웃")
            raise HTTPException(status_code=504, detail="MCP 서버 응답 지연")
        
    return ToolResult(tool=call.tool, output=patched_output)

async def initialize_mcp_session():
    global _mcp_session_id

    async with httpx.AsyncClient() as client:
        res = await client.post(settings.MCP_URL, json={
            "jsonrpc": "2.0",
            "id": "init-001",
            "method": "initialize",
            "params": {
                "protocolVersion": "1.0",
                "capabilities": {},
                "clientInfo": {
                    "name": "agent-core",
                    "version": "1.0"
                }
            }
        }, headers={
            "Accept": "application/json, text/event-stream",
            "Content-Type": "application/json"
        })

        for key, value in res.headers.items():
            if key.lower() == "mcp-session-id":
                _mcp_session_id = value
                break

        if not _mcp_session_id:
            raise RuntimeError("❌ MCP 세션 ID가 응답 헤더에 없음")

        logging.info(f"[✅ MCP 세션 ID 획득] {_mcp_session_id}")
        
        