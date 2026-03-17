import os
from dotenv import load_dotenv

load_dotenv()

CANVAS_BASE_URL = os.getenv("CANVAS_BASE_URL", "").rstrip("/")
CANVAS_TOKEN = os.getenv("CANVAS_TOKEN", "")
MCP_HOST = os.getenv("MCP_HOST", "0.0.0.0")
MCP_PORT = int(os.getenv("MCP_PORT", "8000"))
MCP_SECRET = os.getenv("MCP_SECRET", "")
