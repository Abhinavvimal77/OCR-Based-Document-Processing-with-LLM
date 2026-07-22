# AI-Powered Document Intelligence System (OCR + LLM + Prompt Engineering)

An end-to-end pipeline that extracts text from documents (invoices, resumes, reports) using OCR,
cleans it, and uses an LLM (Google Gemini) to summarize, extract structured data, and answer questions —
with a dedicated demo showing how prompt engineering improves output quality.

## 🎯 Features

- **OCR Extraction**: Extracts text from PDF and image files using Tesseract OCR (PyMuPDF used to render PDF pages as images).
- **Text Cleaning**: Removes OCR noise, collapses whitespace, prepares clean text for the LLM.
- **Summarization**: Generates a concise 5-bullet-point summary of any document.
- **Key Information Extraction**: Extracts structured fields (vendor, client, dates, total amount, currency, line items) as clean JSON — downloadable.
- **Question Answering**: Ask natural language questions about the uploaded document and get grounded answers.
- **Prompt Engineering Showcase**: Side-by-side comparison of a vague/bad prompt vs. a well-engineered prompt on the same document, demonstrating the real-world impact of prompt design on output quality and structure.
- **Simple Web UI**: Built with Streamlit for easy interaction — upload, click, get results.

## 🏗️ Architecture / Workflow

Upload (PDF/Image)
│
▼
ocr.py → Extract raw text (Tesseract + PyMuPDF)
│
▼
utils.py → Clean & normalize text
│
▼
prompts.py → Build task-specific prompts (summary / extraction / Q&A / bad-vs-good)
│
▼
llm.py → Send prompts to Gemini API, parse structured JSON responses
│
▼
app.py → Streamlit UI displays results, JSON download, prompt comparison

## 🛠️ Tech Stack

- **Python 3.13**
- **OCR**: Tesseract (via `pytesseract`) + PyMuPDF (PDF → image conversion)
- **LLM**: Google Gemini API (`gemini-flash-latest`)
- **Frontend**: Streamlit
- **Other**: python-dotenv (API key management), Pillow (image handling)

## 📁 Project Structure

document-ai-project/
│
├── app.py # Streamlit UI
├── ocr.py # OCR extraction (PDF/image → raw text)
├── llm.py # Gemini API wrapper (summarize, extract, Q&A, compare prompts)
├── prompts.py # Prompt templates (bad vs good, summary, Q&A)
├── utils.py # Text cleaning helpers
├── requirements.txt
├── .env # Gemini API key (not committed)
├── sample_docs/ # Sample test documents
└── README.md

## ⚙️ Setup & Installation

1. **Install Tesseract OCR** (system-level, not pip):
   - Windows: https://github.com/UB-Mannheim/tesseract/wiki
   - Mac: `brew install tesseract`
   - Linux: `sudo apt install tesseract-ocr`

   > Note: On Windows, if `tesseract` isn't recognized in your terminal after install,
   > this project hardcodes the path in `ocr.py`:
   > `C:\Program Files\Tesseract-OCR\tesseract.exe`
   > Adjust this path in `ocr.py` if your install location differs.

2. **Get a free Gemini API key**: https://aistudio.google.com/apikey

3. **Clone/copy the project, then install dependencies**:
```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # Mac/Linux
   pip install -r requirements.txt
```

4. **Create a `.env` file** in the project root:

5. **Run the app**:
```bash
   streamlit run app.py
```

## 🎯 Prompt Engineering Highlight

This project explicitly demonstrates prompt engineering principles:

| Bad Prompt | Good Prompt |
|---|---|
| "Extract info from this document" | Explicit field names, format rules ("return only JSON"), hallucination guardrails ("don't guess"), null-handling instructions |
| Inconsistent, unstructured output | Reliable, parseable, structured JSON every time |

This is demoed live in the app under **"Prompt Engineering Demo"**.

## 🚀 Future Improvements

- Multi-document comparison (compare 2 invoices/resumes side by side)
- Resume-specific parsing (skills, experience, education extraction)
- Support for scanned/handwritten documents with improved OCR preprocessing
- Batch processing of multiple documents at once

## 👤 Author

Built as a GenAI / Document AI / Prompt Engineering project demonstrating OCR + LLM integration.