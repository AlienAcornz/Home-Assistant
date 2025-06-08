from fastapi import FastAPI, HTTPException
import log_utils
from pydantic import BaseModel
from typing import List, Dict, Any

# Define a Pydantic model for the incoming log data
class LogEntry(BaseModel):
    message: str
    tag: str

app = FastAPI(
    title="Log API",
    description="A simple API for logging messages with tags and retrieving them.",
    version="1.0.0",
)

@app.get("/", summary="Retrieve all log entries")
def get_all_logs() -> List[Dict[str, Any]]:
    """
    Returns the complete list of log entries.
    Each entry includes a message, timestamp, and a tag.
    """
    return log_utils.get_logs()

@app.get("/filters", summary="Retrieve all unique tags")
def get_filters() -> List[str]:
    """
    Returns a list of all unique tags used across all log entries.
    """
    # It's usually more useful to return unique tags for filters
    return list(set(log_utils.get_tags()))