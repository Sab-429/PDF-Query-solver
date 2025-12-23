from google import genai
from dotenv import load_dotenv
import os, json,requests, numpy as np,joblib
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

EMBEDDINGS_FILE = "embeddings.json"
VECTOR_DB_FILE = "vector_db.joblib"
EMBED_MODEL = "bge-m3"
TOP_K = 10

def embed_query(query):
    payload = {
        "model": EMBED_MODEL,
        "prompt": query
    }
    response = requests.post("http://localhost:11434/api/embeddings", json=payload)
    response.raise_for_status()
    data = response.json()
    return np.array(data["embedding"]).reshape(1, -1)

if os.path.exists(VECTOR_DB_FILE):
    print("Loading vector store from joblib...")
    data = joblib.load(VECTOR_DB_FILE)
    texts = data["texts"]
    embeddings = data["embeddings"]
    metadata = data["metadata"]
    
else:
    print("Building vector store from JSON files...")
    texts, embeddings, metadata = [], [], []
    
    for file in [EMBEDDINGS_FILE]:
        with open(file, "r", encoding="utf-8") as f:
            chunks = json.load(f)
            for chunk in chunks:
                texts.append(chunk["text"])
                embeddings.append(np.array(chunk["embedding"]))
                metadata.append({"id": chunk["id"], "page": chunk["page"]})
    embeddings = np.vstack(embeddings)
    joblib.dump({"texts": texts, "embeddings": embeddings, "metadata": metadata}, VECTOR_DB_FILE)
    print("Vector store saved to joblib.")
    
    print(f"Loaded {len(texts)} chunks")
    
# ================= QUERY =================
query = input("\nAsk a question: ")
query_vec = embed_query(query)

scores = cosine_similarity(query_vec, embeddings).flatten()
top_idx = scores.argsort()[-TOP_K:][::-1]

# ================= BUILD CONTEXT =================
context_blocks = []
references = []

for idx in top_idx:
    block = f"""
[Chunk ID: {metadata[idx]['id']} | Page: {metadata[idx]['page']}]
{texts[idx]}
"""
    context_blocks.append(block.strip())
    references.append(f"- Page {metadata[idx]['page']}, Chunk {metadata[idx]['id']}")

context_text = "\n\n".join(context_blocks)

PROMPT = f"""
You are a PDF Question Answering assistant.

You MUST strictly follow these rules:

RULES:
1. Answer ONLY using the provided PDF chunks.
2. Do NOT use outside knowledge.
3. If the answer is NOT found in the chunks, reply exactly:
   "The answer is not available in the provided PDF."
4. Use the chunk text verbatim where possible.
5. ALWAYS cite metadata (page number and chunk id).

USER QUESTION:
{query}

PDF CHUNKS:
{context_text}

INSTRUCTIONS FOR ANSWER FORMAT:
- Start with a clear explanation.
- Then list references in this exact format:

References:
- Page <page_number>, Chunk <chunk_id>
- Page <page_number>, Chunk <chunk_id>

FINAL ANSWER:
"""
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[PROMPT]
)
answer = response.text.strip()
print("\n", answer)

with open("query_output.txt", "w", encoding="utf-8") as f:
    f.write(answer)