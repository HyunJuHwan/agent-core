TOOL_LIST = [
    {
        "tool": "createCharacter",
        "input": {
            "style": "2d | 3d",
            "prompt": "캐릭터 설명 문자열"
        }
    },
    {
        "tool": "createScene",
        "input": {
            "character_ids": "[string]",
            "scene_description": "장면 설명 문자열"
        }
    },
    # {
    #     "tool": "updateCharacter",
    #     "input": {
    #         "old_character_id": "string",
    #         "prompt": "변경할 캐릭터 설명 문자열",
    #         "style": "2d | 3d"
    #     }
    # },
    # {
    #     "tool": "confirmCharacter",
    #     "input": {
    #         "character_ids": "[string]"
    #     }
    # },
    {
        "tool": "buildWebtoon",
        "input": {
            "scene_ids": "[string]",
            "speech_bubbles": "[{ scene_id: string; text: string }] (선택 사항)"
        }
    },
    {
        "tool": "buildVideo",
        "input": {
            "frame_folder": "scene"
        }
    }
]