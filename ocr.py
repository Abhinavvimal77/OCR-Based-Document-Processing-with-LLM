import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import os

# ---- Hardcoded Tesseract path (Windows) ----
# Since PATH setup was inconsistent, we point directly to the exe.
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text_from_image(image: Image.Image) -> str:
    """Run OCR on a single PIL Image and return extracted text."""
    text = pytesseract.image_to_string(image)
    return text


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Convert each page of a PDF to an image using PyMuPDF,
    then run OCR on each page. Returns combined text from all pages.
    """
    full_text = ""
    doc = fitz.open(pdf_path)

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)

        # Render page to an image (zoom=2 for better OCR accuracy)
        zoom = 2
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)

        # Convert PyMuPDF pixmap -> PIL Image
        img_bytes = pix.tobytes("png")
        image = Image.open(io.BytesIO(img_bytes))

        page_text = extract_text_from_image(image)
        full_text += f"\n--- Page {page_num + 1} ---\n{page_text}"

    doc.close()
    return full_text


def extract_text_from_image_file(image_path: str) -> str:
    """Load an image file from disk and run OCR on it."""
    image = Image.open(image_path)
    return extract_text_from_image(image)


def extract_text(file_path: str) -> str:
    """
    Main entry point. Detects file type (PDF or image) and
    routes to the correct extraction function.
    """
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext in [".png", ".jpg", ".jpeg", ".bmp", ".tiff"]:
        return extract_text_from_image_file(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")


# ---- Quick manual test ----
if __name__ == "__main__":
    test_file = "sample_docs/invoice.png"  # change to your test file
    if os.path.exists(test_file):
        result = extract_text(test_file)
        print("Extracted Text:\n")
        print(result)
    else:
        print(f"Test file not found: {test_file}. Put a sample PDF/image in sample_docs/ to test.")