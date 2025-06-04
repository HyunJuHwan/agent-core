class AliasMapper:
    def __init__(self):
        self.map = {}
        self.counters = {"c": 1, "s": 1}

    def register(self, tool: str, real_id: str):
        prefix = "c" if "Character" in tool else "s"
        alias = f"{prefix}-{self.counters[prefix]}"
        self.map[alias] = real_id
        self.counters[prefix] += 1
        return alias

    def resolve(self, id_list: list[str]) -> list[str]:
        return [self.map.get(i, i) for i in id_list]

    def resolve_scene_bubbles(self, bubbles: list[dict]) -> list[dict]:
        for bubble in bubbles:
            sid = bubble.get("scene_id")
            if sid:
                bubble["scene_id"] = self.map.get(sid, sid)
        return bubbles
