import json
import time
import os
from datetime import datetime, timezone

LOG_PATH = os.getenv("LOG_PATH", "/shared/logs/app.log")

os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

while True:
    log = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "service": "myapp",
        "level": "INFO",
        "message": "hello from application"
    }
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(log) + "\n")
    time.sleep(1)

