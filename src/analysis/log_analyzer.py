import re
from src.config.logger import setup_logger

logger = setup_logger(__name__)

def extract_warnings_errors(text: str):
    """Finds warnings and errors using regex."""
    warnings = re.findall(r"\bWARNING[:\]]?(.*)", text, flags=re.IGNORECASE)
    errors = re.findall(r"\bERROR[:\]]?(.*)", text, flags=re.IGNORECASE)
    return warnings, errors

def summarize_performance(text: str):
    """Simple performance heuristics."""
    cpu_usage = re.findall(r"(?:CPU\s*usage|CPU\s*utilization)[^\d]*(\d+%)", text, re.IGNORECASE)
    memory = re.findall(r"(?:memory\s*usage|used\s*memory)[^\d]*(\d+MB|\d+GB|\d+%)", text, re.IGNORECASE)
    return {"CPU Usage": cpu_usage, "Memory Usage": memory}

def get_advanced_insights(text: str):
    """Mockup for future prediction and insights."""
    insights = []
    if "OutOfMemory" in text:
        insights.append("Potential memory leak — monitor allocation and GC logs.")
    if "timeout" in text.lower():
        insights.append("Increase server timeout settings or check network latency.")
    return insights
