import pdfplumber

def extract_text_from_pdf(pdf_path):
    pages_data = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if text:
                pages_data.append({
                    "page": page_number,
                    "text": text.strip()
                })

    return pages_data
