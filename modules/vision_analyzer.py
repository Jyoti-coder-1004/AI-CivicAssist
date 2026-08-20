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
    / "vision_analysis.txt"
)


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv(
    PROJECT_ROOT / ".env"
)

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


# ============================================================
# MODEL
# ============================================================

MODEL_NAME = "gemini-2.5-flash"


# ============================================================
# LOAD VISION PROMPT
# ============================================================

def load_vision_prompt(description: str = "") -> str:

    if not PROMPT_FILE.exists():

        raise FileNotFoundError(
            f"Vision prompt file not found at:\n"
            f"{PROMPT_FILE}"
        )

    with PROMPT_FILE.open(
        "r",
        encoding="utf-8"
    ) as file:

        template = file.read()

    return template.format(
        description=(
            description.strip()
            if description
            else "No additional description provided."
        )
    )


# ============================================================
# IMAGE ANALYSIS
# ============================================================

def analyze_civic_image(
    image_bytes: bytes,
    mime_type: str,
    description: str = "",
) -> str:

    prompt = load_vision_prompt(
        description
    )

    image_part = types.Part.from_bytes(
        data=image_bytes,
        mime_type=mime_type,
    )

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[
            prompt,
            image_part,
        ],
    )

    if not response.text:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return response.text