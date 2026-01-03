from app.services.textbook_loader import extract_text_from_pdf

data = extract_text_from_pdf(
    "data/textbooks/raw_pdfs/grade10_science_en.pdf"
)

print(data[0])
