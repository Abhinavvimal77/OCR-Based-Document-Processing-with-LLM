import streamlit as st
import json
import tempfile
import os

from ocr import extract_text
from utils import clean_text, word_count
from llm import summarize_document, extract_key_info, ask_question, compare_prompts

st.set_page_config(page_title="AI Document Intelligence System", layout="wide")

st.title("📄 AI-Powered Document Intelligence System")
st.caption("OCR + LLM + Prompt Engineering — Upload an invoice, resume, or report to get started.")

# ---------------------------------------------------------
# Session state to persist extracted text across reruns
# ---------------------------------------------------------
if "raw_text" not in st.session_state:
    st.session_state.raw_text = None
if "cleaned_text" not in st.session_state:
    st.session_state.cleaned_text = None

# ---------------------------------------------------------
# 1. File Upload
# ---------------------------------------------------------
uploaded_file = st.file_uploader(
    "Upload a document (PDF, PNG, JPG)",
    type=["pdf", "png", "jpg", "jpeg"]
)

if uploaded_file is not None:
    # Save uploaded file to a temp path so ocr.py can read it
    suffix = os.path.splitext(uploaded_file.name)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    with st.spinner("Running OCR on your document..."):
        raw_text = extract_text(tmp_path)
        cleaned = clean_text(raw_text)

    st.session_state.raw_text = raw_text
    st.session_state.cleaned_text = cleaned

    os.remove(tmp_path)  # cleanup temp file

    st.success(f"Document processed! ({word_count(cleaned)} words extracted)")

# ---------------------------------------------------------
# 2. Show Raw vs Cleaned Text
# ---------------------------------------------------------
if st.session_state.cleaned_text:
    tab1, tab2 = st.tabs(["🧹 Cleaned Text", "📝 Raw OCR Text"])
    with tab1:
        st.text_area("Cleaned text", st.session_state.cleaned_text, height=250)
    with tab2:
        st.text_area("Raw OCR output", st.session_state.raw_text, height=250)

    st.divider()

    # -----------------------------------------------------
    # 3. LLM Features
    # -----------------------------------------------------
    st.header("🤖 AI Analysis")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📋 Summarize Document"):
            with st.spinner("Summarizing..."):
                summary = summarize_document(st.session_state.cleaned_text)
            st.markdown("### Summary")
            st.markdown(summary)

    with col2:
        if st.button("🔑 Extract Key Info (JSON)"):
            with st.spinner("Extracting structured data..."):
                data = extract_key_info(st.session_state.cleaned_text)
            st.markdown("### Extracted Fields")
            st.json(data)
            st.download_button(
                "⬇️ Download JSON",
                data=json.dumps(data, indent=2),
                file_name="extracted_data.json",
                mime="application/json"
            )

    with col3:
        st.markdown("**❓ Ask a Question**")
        question = st.text_input("e.g. What is the total amount?", key="qa_input")
        if st.button("Get Answer") and question:
            with st.spinner("Thinking..."):
                answer = ask_question(st.session_state.cleaned_text, question)
            st.markdown("### Answer")
            st.markdown(answer)

    st.divider()

    # -----------------------------------------------------
    # 4. Prompt Engineering Showcase
    # -----------------------------------------------------
    st.header("🎯 Prompt Engineering Demo")
    st.caption("See the difference a well-engineered prompt makes on the SAME document.")

    if st.button("⚖️ Compare Bad Prompt vs Good Prompt"):
        with st.spinner("Running both prompts..."):
            result = compare_prompts(st.session_state.cleaned_text)

        col_bad, col_good = st.columns(2)

        with col_bad:
            st.markdown("#### ❌ Bad Prompt")
            st.code(result["bad_prompt"], language="text")
            st.markdown("**Output:**")
            st.text(result["bad_response"])

        with col_good:
            st.markdown("#### ✅ Good Prompt")
            st.code(result["good_prompt"], language="text")
            st.markdown("**Output:**")
            st.code(result["good_response"], language="json")

        st.info(
            "Notice how the bad prompt gives an unstructured, inconsistent response, "
            "while the good prompt reliably returns clean, structured JSON with explicit fields."
        )

else:
    st.info("👆 Upload a document above to get started.")