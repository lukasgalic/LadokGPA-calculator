from PyPDF2 import PdfReader


pdf_file = "Records.pdf"
reader = PdfReader(pdf_file)

for page in reader.pages:
    print(page.extract_text())
