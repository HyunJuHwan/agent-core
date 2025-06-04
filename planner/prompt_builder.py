from utils.tool_catalog import TOOL_LIST
from pathlib import Path

def build_prompt(user_prompt: str) -> tuple[str, str]:
    system_template = Path("prompt_templates/system_tool_planner.txt").read_text()
    tool_list_str = "\n".join([f"- {t['tool']}: {t['input']}" for t in TOOL_LIST])

    system_prompt = system_template.replace("{{ .ToolList }}", tool_list_str)
    return system_prompt, user_prompt
