step by step pipeline
read_pdf.py
    |
    |
    |
create_chunks.py
    |
    |
    |
embed_chunks.py
    |
    |
    |
query.py

=============== Tech Stack ================

Python 3.10+

Google Gemini / LLM

Vector Embeddings

Cosine Similarity

RAG Architecture

python-dotenv

PyPDF

sckit-learn

=============Flowchart===========
┌─────────────────────┐
│   User Input        │
│     (PDF)           │
└─────────┬───────────┘
          │
          ▼
┌──────────────────────────┐
│   File Ingestion Layer   │
│                          │
│  • Read PDF              │
│  • Validate file format  │
└─────────┬────────────────┘
          │
          ▼
┌──────────────────────────┐
│   Content Extraction     │
│                          │
│  PDF → Text              │
│                          │
└─────────┬────────────────┘
          │
          ▼
┌──────────────────────────┐
│   Text Cleaning Layer    │
│                          │
│  • Remove noise          │
│  • Normalize text        │
│  • Translate to English  │
└─────────┬────────────────┘
          │
          ▼
┌──────────────────────────┐
│   Chunking Engine        │
│                          │
│  • Split text into       │
│    semantic chunks       │
│  • Add metadata          │
│    (id, page, text)      │
└─────────┬────────────────┘
          │
          ▼
┌──────────────────────────┐
│   Embedding Generator    │
│                          │
│  • Convert chunks →      │
│    vector embeddings     │
│  • Store in vector DB    │
└─────────┬────────────────┘
          │
          ▼
┌──────────────────────────┐
│   Vector Store           │
│                          │
│  • embeddings.json       │
│  • metadata              │
└─────────┬────────────────┘
          │
          ▼
┌──────────────────────────┐
│   User Query             │
│                          │
│  • Natural language Q    │
└─────────┬────────────────┘
          │
          ▼
┌──────────────────────────┐
│   Query Embedding        │
│                          │
│  • Convert question →    │
│    embedding vector      │
└─────────┬────────────────┘
          │
          ▼
┌──────────────────────────┐
│   Similarity Search      │
│                          │
│  • Cosine similarity     │
└─────────┬────────────────┘
          │
          ▼
┌──────────────────────────┐
│   Context Builder        │
│                          │
│  • Combine top chunks    │
│  • Create LLM prompt     │
└─────────┬────────────────┘
          │
          ▼
┌──────────────────────────┐
│   LLM Response Generator │
│       (gemini api)       │
│  • Uses only retrieved   │
│    document context      │
│  • No hallucination      │
└─────────┬────────────────┘
          │
          ▼
┌──────────────────────────┐
│   Final Answer Output    │
│                          │
│  • Accurate              │
│  • Explainable           │
│  • Source-aware          │
└──────────────────────────┘


Example ----> how does it response

Ask a question: what is the composition of white portland cement?

White Portland cement is composed of dicalcium silicate (C2S, ~ 60%), tricalcium silicate (C3S, ~20-30 %), and tricalcium alluminate (C3A, ~ 10%), along with the absence of iron oxide.

References:
- Page 18, Chunk 33