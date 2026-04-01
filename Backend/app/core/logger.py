import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict
from app.core.config import settings

class JSONLLogger:
    def __init__(self, log_name: str = "processing_logs.jsonl"):
        self.log_file = settings.logs_dir / log_name

    def log(self, step: str, status: str, details: Any = None):
        """
        Logs a processing step to a JSONL file.
        """
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "step": step,
            "status": status,
            "details": details
        }
        
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")

# Global logger instance
logger = JSONLLogger()
