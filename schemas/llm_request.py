from pydantic import BaseModel
from typing import List, Optional

class LLMRequest(BaseModel):
    model: str  # 사용할 LLM 모델 이름 (예: gemma3-custom)
    prompt: Optional[str] = None  # 단일 프롬프트 (예: tool planner 스타일)
    messages: Optional[List[dict]] = None  # 대화형 LLM일 경우 (role + content)
    system: Optional[str] = None  # system message (역할, 도구 제약 등)
    stream: bool = False  # 스트리밍 여부 (기본 False)
