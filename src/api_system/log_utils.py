# src/api_system/log_utils.py  (same file used by both Main & API)

import datetime
import json
from pathlib import Path
from threading import Lock

LOG_FILE = Path(__file__).parent / "logs.json"
_file_lock = Lock()

def add_log(message: str, tag: str):
    """Call this from your Main process wherever you need to log."""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = {"time": now, "tag": tag, "message": message}

    with _file_lock:
        if LOG_FILE.exists():
            try:
                data = json.loads(LOG_FILE.read_text())
            except json.JSONDecodeError:
                data = []
        else:
            data = []

        data.append(entry)
        LOG_FILE.write_text(json.dumps(data, indent=2))

def get_logs():
    """Call this in your API to serve /logs."""
    print("Logs received!")
    if not LOG_FILE.exists():
        return []
    try:
        return json.loads(LOG_FILE.read_text())
    except json.JSONDecodeError:
        return []

def get_tags():
    logs = get_logs()
    return list({entry["tag"] for entry in logs})
