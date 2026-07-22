import re


def clean_text(raw_text: str) -> str:
    """
    Cleans raw OCR text:
    - Removes excessive blank lines
    - Strips trailing/leading whitespace per line
    - Collapses multiple spaces into one
    - Removes weird OCR artifacts (stray special characters)
    """
    if not raw_text:
        return ""

    # Strip trailing/leading whitespace on each line
    lines = [line.strip() for line in raw_text.splitlines()]

    # Remove empty lines (but keep single blank lines between sections)
    cleaned_lines = []
    prev_blank = False
    for line in lines:
        if line == "":
            if not prev_blank:
                cleaned_lines.append("")
            prev_blank = True
        else:
            cleaned_lines.append(line)
            prev_blank = False

    cleaned_text = "\n".join(cleaned_lines)

    # Collapse multiple spaces into a single space
    cleaned_text = re.sub(r"[ \t]+", " ", cleaned_text)

    # Remove common OCR noise characters (keep punctuation that matters for invoices: . , $ % : / -)
    cleaned_text = re.sub(r"[^\w\s.,$%:/\-\n]", "", cleaned_text)

    return cleaned_text.strip()


def chunk_text(text: str, max_chars: int = 6000) -> list[str]:
    """
    Splits long text into chunks under max_chars length,
    breaking at paragraph boundaries where possible.
    Useful if a document is too long for a single LLM call.
    """
    if len(text) <= max_chars:
        return [text]

    chunks = []
    current_chunk = ""

    for paragraph in text.split("\n\n"):
        if len(current_chunk) + len(paragraph) + 2 <= max_chars:
            current_chunk += paragraph + "\n\n"
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = paragraph + "\n\n"

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def word_count(text: str) -> int:
    """Returns the number of words in a text block."""
    return len(text.split())


# ---- Quick manual test ----
if __name__ == "__main__":
    sample = """
    Invoice



    Dream Design,   126 Industry Road, Auckland



    BILL TO

    Total due (NZD)     1 060,00 $
    """
    print("BEFORE:")
    print(repr(sample))
    print("\nAFTER:")
    print(repr(clean_text(sample)))
    print("\nWord count:", word_count(clean_text(sample)))