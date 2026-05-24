from pypdf import PdfReader
import sys

if len(sys.argv) < 2:
    print("Usage: python test_pdf_extract.py your_file.pdf")
    sys.exit(1)

pdf_path = sys.argv[1]
reader = PdfReader(pdf_path)

for page_number, page in enumerate(reader.pages, start=1):
    text = page.extract_text() or ""
    print(f"\n--- Page {page_number} ---")
    print(text[:1000])
