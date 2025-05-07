import os
import json
from datetime import datetime

def save_session(session_id, data):
    os.makedirs("storage/logs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"storage/logs/session_{session_id[:8]}_{timestamp}.json"

    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
