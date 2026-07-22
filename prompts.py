# =========================================================
# PROMPT ENGINEERING SHOWCASE
# Demonstrates the difference between a "bad" vague prompt
# and a "good" well-engineered prompt for the same task.
# =========================================================

# ---------------------------------------------------------
# 1. BAD vs GOOD prompt for key information extraction
# ---------------------------------------------------------

BAD_EXTRACTION_PROMPT = """
Extract info from this document:

{document_text}
"""

GOOD_EXTRACTION_PROMPT = """
You are a precise document data extraction assistant.

From the document text below, extract the following fields:
- vendor_name (the company issuing the invoice/document)
- client_name (the person/company being billed, if present)
- date (the issue date, format as DD-MM-YYYY if possible)
- due_date (if present, format as DD-MM-YYYY)
- total_amount (the final total amount due, as a number, no currency symbol)
- currency (e.g. USD, NZD, INR)
- line_items (a list of items/services with description, quantity, unit_price, amount if present)

Rules:
- If a field is not found in the document, set its value to null.
- Do NOT guess or hallucinate values that are not present in the text.
- Return ONLY valid JSON. No explanation, no markdown code fences, no extra text.

Document text:
\"\"\"
{document_text}
\"\"\"

Return the JSON now:
"""


# ---------------------------------------------------------
# 2. Summarization prompt
# ---------------------------------------------------------

SUMMARY_PROMPT = """
You are a helpful assistant that summarizes documents concisely.

Summarize the following document in exactly 5 clear bullet points.
Focus on the most important facts: who is involved, what the document is about,
key dates, and key figures/amounts if present.

Document text:
\"\"\"
{document_text}
\"\"\"

Return only the 5 bullet points, nothing else.
"""


# ---------------------------------------------------------
# 3. Question Answering prompt
# ---------------------------------------------------------

QA_PROMPT = """
You are a helpful assistant answering questions about a specific document.
Only use information found in the document text below. If the answer is not
present in the document, say "This information is not present in the document."

Document text:
\"\"\"
{document_text}
\"\"\"

Question: {question}

Answer concisely and directly:
"""


# ---------------------------------------------------------
# Helper functions to fill in the templates
# ---------------------------------------------------------

def build_bad_extraction_prompt(document_text: str) -> str:
    return BAD_EXTRACTION_PROMPT.format(document_text=document_text)


def build_good_extraction_prompt(document_text: str) -> str:
    return GOOD_EXTRACTION_PROMPT.format(document_text=document_text)


def build_summary_prompt(document_text: str) -> str:
    return SUMMARY_PROMPT.format(document_text=document_text)


def build_qa_prompt(document_text: str, question: str) -> str:
    return QA_PROMPT.format(document_text=document_text, question=question)