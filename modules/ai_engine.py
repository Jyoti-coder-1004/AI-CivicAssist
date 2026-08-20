import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")


if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is missing. "
        "Please add it to your .env file."
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
# PROMPT LOADER
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent


def load_prompt(filename: str) -> str:
    """Load a prompt template from the prompts directory."""

    prompt_path = BASE_DIR / "prompts" / filename

    with open(
        prompt_path,
        "r",
        encoding="utf-8",
    ) as file:

        return file.read()


# ============================================================
# GEMINI REQUEST
# ============================================================

def generate_ai_response(prompt: str) -> str:
    """Send a prompt to Gemini and return the response."""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )

    return response.text


# ============================================================
# ISSUE ANALYSIS
# ============================================================

def analyze_issue(description: str) -> str:

    template = load_prompt(
        "issue_analysis.txt"
    )

    prompt = template.format(
        description=description
    )

    return generate_ai_response(prompt)


# ============================================================
# SEVERITY ANALYSIS
# ============================================================

def analyze_severity(
    issue: str,
    category: str,
    location: str,
) -> str:

    template = load_prompt(
        "severity_analysis.txt"
    )

    prompt = template.format(
        issue=issue,
        category=category,
        location=location,
    )

    return generate_ai_response(prompt)


# ============================================================
# RECOMMENDATION
# ============================================================

def generate_recommendation(
    issue: str,
    category: str,
    severity: str,
) -> str:

    template = load_prompt(
        "recommendation.txt"
    )

    prompt = template.format(
        issue=issue,
        category=category,
        severity=severity,
    )

    return generate_ai_response(prompt)