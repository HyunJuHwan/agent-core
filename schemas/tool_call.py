from pydantic import BaseModel
from typing import Dict, Any

class ToolCall(BaseModel):
    tool: str
    input: Dict[str, Any]

class ToolResult(BaseModel):
    tool: str
    output: Dict[str, Any]
