import json
import os

class RKTrainer:
    def __init__(self, patterns_file="patterns.json", logs_file="query_logs.json"):
        self.patterns_file = patterns_file
        self.logs_file = logs_file

    def log_query(self, query, intent, handled_by):
        log_entry = {
            "query": query,
            "intent": intent,
            "handled_by": handled_by,
            "timestamp": str(os.path.getmtime(self.patterns_file)) if os.path.exists(self.patterns_file) else "0"
        }
        
        logs = []
        if os.path.exists(self.logs_file):
            try:
                with open(self.logs_file, "r", encoding="utf-8") as f:
                    logs = json.load(f)
            except:
                pass
        
        logs.append(log_entry)
        with open(self.logs_file, "w", encoding="utf-8") as f:
            json.dump(logs[-100:], f, indent=4) # Keep last 100

    def add_custom_pattern(self, intent_type, pattern):
        """Allows dynamic updating of patterns.json"""
        if not os.path.exists(self.patterns_file):
            return False
            
        try:
            with open(self.patterns_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            if intent_type in data:
                if isinstance(data[intent_type], list):
                    if pattern not in data[intent_type]:
                        data[intent_type].append(pattern)
                elif isinstance(data[intent_type], dict):
                    # Handle nested dicts like SYSTEM_COMMAND
                    pass
            
            with open(self.patterns_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            return True
        except:
            return False

if __name__ == "__main__":
    trainer = RKTrainer()
    trainer.log_query("test query", "UNKNOWN", "brain")
    print("Logged test query.")
