import json
import requests
import numpy as np
import time

CHUNKS_FILE = "chunks.json"
EMBEDDINGS_FILE = "embeddings.json"

EMBEDDING_MODEL = "bge-m3"
OLLAMA_URL = "http://localhost:11434/api/embeddings"

with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
    chunks = json.load(f)
    
embedded_chunks = []
def get_embedding(text):
    payload = {
        "model": EMBEDDING_MODEL,
        "prompt": text
    }
    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()
    data = response.json()
    return data["embedding"]

for i, chunk in enumerate(chunks):
    embedding = get_embedding(chunk["text"])
    embedded_chunks.append({
        "id": chunk["id"],
        "page": chunk["page"],
        "text": chunk["text"],
        "embedding": embedding
    })
    if (i + 1) % 10 == 0:
        print(f"Processed {i + 1}/{len(chunks)} chunks")
    time.sleep(0.1)  # To avoid overwhelming the server

with open(EMBEDDINGS_FILE, "w", encoding="utf-8") as f:
    json.dump(embedded_chunks, f, indent=2, ensure_ascii=False) 
    
print(f"Saved embeddings for {len(embedded_chunks)} chunks to {EMBEDDINGS_FILE}")
