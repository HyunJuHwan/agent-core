from context.store import context_store
from schemas.tool_call import ToolCall, ToolResult

class ConversationManager:
    def __init__(self, user_id: str):
        self.user_id = user_id

    def get_history(self) -> list[dict]:
        return context_store.get_conversation(self.user_id)

    def add_user_prompt(self, prompt: str):
        context_store.append_to_conversation(self.user_id, [
            {"role": "user", "content": prompt}
        ])

    def add_tool_plan(self, tool_calls: list[ToolCall]):
        calls = [call.model_dump() for call in tool_calls]
        context_store.append_to_conversation(self.user_id, [
            {"role": "assistant", "tool_calls": calls}
        ])

    def add_tool_result(self, result: ToolResult):
        context_store.append_to_conversation(self.user_id, [
            {
                "role": "tool",
                "tool": result.tool,
                "output": result.output
            }
        ])
