from pypdf import PdfReader

PDF_PATH = "sample.pdf"
OUTPUT_FILE = "output.txt"

reader = PdfReader(PDF_PATH)

all_text = []

for page_number, page in enumerate(reader.pages, start=1):
    text = page.extract_text()
    if text:
        all_text.append(f"\n--- Page {page_number} ---\n{text}")

full_text = "\n".join(all_text)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(full_text)

print(f"Extracted {len(reader.pages)} pages into {OUTPUT_FILE}")

