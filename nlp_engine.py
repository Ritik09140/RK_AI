import re
import json
import os

class RKNLP:
    def __init__(self, patterns_file="patterns.json"):
        self.patterns_file = patterns_file
        self.patterns = self.load_patterns()
        
    def load_patterns(self):
        default_patterns = {
            "OPEN_APP": [
                r"(?:open|kholo|chalao|launch|start)\s+([a-zA-Z\s]+)",
                r"([a-zA-Z\s]+)\s+(?:kholo|chalao|launch|start)"
            ],
            "PLAY_YOUTUBE": [
                r"(?:play|chalao|search on youtube)\s+([a-zA-Z0-9\s]+)",
                r"([a-zA-Z0-9\s]+)\s+on\s+youtube",
                r"youtube\s+(?:par|pe)\s+([a-zA-Z0-9\s]+)\s+(?:song|video|chalao)"
            ],
            "SEARCH_GOOGLE": [
                r"(?:search|khojo|find)\s+(?:on google)?\s+([a-zA-Z0-9\s]+)",
                r"([a-zA-Z0-9\s]+)\s+(?:search karo|google par)"
            ],
            "SYSTEM_COMMAND": {
                "shutdown": [r"shutdown", r"pc band", r"system band"],
                "restart": [r"restart", r"reboot"],
                "volume_up": [r"volume up", r"awaz badhao", r"volume badhao"],
                "volume_down": [r"volume down", r"awaz kam", r"volume kam"],
                "mute": [r"mute", r"chup karo"],
                "screenshot": [r"screenshot", r"screen capture", r"snap"]
            },
            "TIME_INFO": [r"time", r"kitne baje", r"samay", r"waqt", r"date", r"tarikh", r"aaj ki tarikh"]
        }
        
        if os.path.exists(self.patterns_file):
            try:
                with open(self.patterns_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return default_patterns
        return default_patterns

    def detect_intent(self, text):
        t = text.lower().strip()
        
        # 1. System Commands (High Priority)
        for cmd, patterns in self.patterns["SYSTEM_COMMAND"].items():
            for p in patterns:
                if re.search(p, t):
                    return {"intent": f"SYSTEM_{cmd.upper()}", "params": {}}

        # 2. Open App
        for p in self.patterns["OPEN_APP"]:
            match = re.search(p, t)
            if match:
                return {"intent": "OPEN_APP", "params": {"target": match.group(1).strip()}}

        # 3. Play YouTube
        for p in self.patterns["PLAY_YOUTUBE"]:
            match = re.search(p, t)
            if match:
                return {"intent": "PLAY_YOUTUBE", "params": {"query": match.group(1).strip()}}

        # 4. Search Google
        for p in self.patterns["SEARCH_GOOGLE"]:
            match = re.search(p, t)
            if match:
                return {"intent": "SEARCH_GOOGLE", "params": {"query": match.group(1).strip()}}

        # 5. Time & Date
        for p in self.patterns["TIME_INFO"]:
            if re.search(p, t):
                return {"intent": "GET_TIME", "params": {}}

        return {"intent": "UNKNOWN", "params": {}}
    
if __name__ == "__main__":
    nlp = RKNLP()
    print(nlp.detect_intent("RK, youtube par python tutorial chalao"))
    print(nlp.detect_intent("kholo chrome"))
    print(nlp.detect_intent("shutdown pc"))
