import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

PROMPT_FILE = (
    PROJECT_ROOT
    / "prompts"
    / "voice_analysis.txt"
)


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv(PROJECT_ROOT / ".env")

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is missing. "
        "Please check your .env file."
    )


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client(
    api_key=API_KEY
)


MODEL_NAME = "gemini-2.5-flash"


# ============================================================
# LOAD PROMPT
# ============================================================

def load_voice_prompt() -> str:

    if not PROMPT_FILE.exists():
        raise FileNotFoundError(
            f"Voice prompt file not found:\n"
            f"{PROMPT_FILE}"
        )

    with PROMPT_FILE.open(
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()


# ============================================================
# VOICE ANALYSIS
# ============================================================

def analyze_voice_report(
    audio_bytes: bytes,
    mime_type: str = "audio/wav",
) -> str:

    prompt = load_voice_prompt()

    audio_part = types.Part.from_bytes(
        data=audio_bytes,
        mime_type=mime_type,
    )

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[
            prompt,
            audio_part,
        ],
    )

    if not response.text:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return response.text