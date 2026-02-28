import pdfplumber

def extract_text_from_pdf(file):
    text = ""

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    # Clean text
    text = text.strip()
    text = " ".join(text.split())

    # Limit characters (important for Gemini token control)
    return text[:7000]