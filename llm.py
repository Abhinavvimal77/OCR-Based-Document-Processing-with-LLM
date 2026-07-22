import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

from prompts import (
    build_bad_extraction_prompt,
    build_good_extraction_prompt,
    build_summary_prompt,
    build_qa_prompt,
)

# ---- Load API key from .env ----
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found. Make sure your .env file has GEMINI_API_KEY=your_key")

genai.configure(api_key=GEMINI_API_KEY)

# Using a fast, free-tier friendly model
MODEL_NAME = "models/gemini-flash-latest"
model = genai.GenerativeModel(MODEL_NAME)


def _call_gemini(prompt: str) -> str:
    """Low-level call to Gemini, returns raw text response."""
    response = model.generate_content(prompt)
    return response.text.strip()


def summarize_document(document_text: str) -> str:
    """Returns a 5-bullet-point summary of the document."""
    prompt = build_summary_prompt(document_text)
    return _call_gemini(prompt)


def extract_key_info(document_text: str) -> dict:
    """
    Uses the GOOD (well-engineered) prompt to extract structured fields.
    Returns a Python dict (parsed from the JSON the LLM returns).
    """
    prompt = build_good_extraction_prompt(document_text)
    raw_response = _call_gemini(prompt)

    # Clean up in case the model still wraps JSON in markdown fences
    cleaned = raw_response.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:].strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # If parsing fails, return the raw text so the user can still see something
        return {"error": "Failed to parse JSON", "raw_response": raw_response}


def ask_question(document_text: str, question: str) -> str:
    """Answers a specific question about the document."""
    prompt = build_qa_prompt(document_text, question)
    return _call_gemini(prompt)


def compare_prompts(document_text: str) -> dict:
    """
    Runs BOTH the bad prompt and the good prompt on the same document
    so we can show the accuracy/quality difference side by side.
    """
    bad_prompt = build_bad_extraction_prompt(document_text)
    good_prompt = build_good_extraction_prompt(document_text)

    bad_response = _call_gemini(bad_prompt)
    good_response = _call_gemini(good_prompt)

    return {
        "bad_prompt": bad_prompt,
        "bad_response": bad_response,
        "good_prompt": good_prompt,
        "good_response": good_response,
    }


# ---- Quick manual test ----
if __name__ == "__main__":
    sample_text = """
    Invoice
    Dream Design, 126 Industry Road, Auckland 1061, New Zealand
    BILL TO Your client, 75 Hamlin Road, Auckland 1060, New Zealand
    Invoice No. 2022022
    Issue date 20.7.2023
    Due date 3.8.2023
    Description: Brand illustrations, Brand logo, Ad banners design
    Total due (NZD): 1060,00 $
    """

    print("=== SUMMARY ===")
    print(summarize_document(sample_text))

    print("\n=== KEY INFO EXTRACTION (structured JSON) ===")
    print(json.dumps(extract_key_info(sample_text), indent=2))

    print("\n=== Q&A TEST ===")
    print(ask_question(sample_text, "What is the total amount due?"))