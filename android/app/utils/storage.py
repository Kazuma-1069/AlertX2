import json
import os

STORAGE_FILE = "alertx_local_store.json"

class LocalStore:
    def __init__(self, filepath=STORAGE_FILE):
        self.filepath = filepath
        self.data = self._load()

    def _load(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.data, f)

local_store = LocalStore()
