import datetime
import json
from pathlib import Path

LOG_FILE = Path(__file__).parent / "logs.json"

def _load_logs():
    if LOG_FILE.exists():
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    return []

def _save_logs(logs):
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f)

def add_log(message: str, tag: str):
    logs = _load_logs()
    now = datetime.datetime.now().strftime("%H:%M:%S")
    logs.append({"message": message, "time": now, "tag": tag})
    _save_logs(logs)

def get_logs():
    logs = _load_logs()
    print("Logs received!")
    return logs

def get_tags():
    return list({entry["tag"] for entry in _load_logs()})
