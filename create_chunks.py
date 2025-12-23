from pypdf import PdfReader
import json
import re

reader = PdfReader("sample.pdf")

MAX_CHARS = 800
chunks = []
chunk_id = 0

for page_no, page in enumerate(reader.pages, start=1):
    text = page.extract_text()
    if not text:
        continue

    sentences = re.split(r'(?<=[.!?])\s+', text)
    current = []
    length = 0

    for s in sentences:
        if length + len(s) <= MAX_CHARS:
            current.append(s)
            length += len(s)
        else:
            chunks.append({
                "id": chunk_id,
                "page": page_no,
                "text": " ".join(current).strip()
            })
            chunk_id += 1
            current = [s]
            length = len(s)

    if current:
        chunks.append({
            "id": chunk_id,
            "page": page_no,
            "text": " ".join(current).strip()
        })
        chunk_id += 1

with open("chunks.json", "w", encoding="utf-8") as f:
    json.dump(chunks, f, indent=2, ensure_ascii=False)

print(f"Created {len(chunks)} page-aware chunks")
