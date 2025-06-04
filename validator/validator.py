from schemas.tool_call import ToolCall

def validate_call(call: ToolCall) -> bool:
    # 최소한의 유효성 검사
    if not call.tool or not isinstance(call.input, dict):
        return False
    return True
