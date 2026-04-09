import os, pathlib
from dotenv import load_dotenv

BASE = pathlib.Path(__file__).parent.parent / "rk_ai"
print("Loading from:", BASE.parent / ".env")
load_dotenv(BASE.parent / ".env")
print("KEY:", os.getenv("GEMINI_API_KEY"))
