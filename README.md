# 📄🔍 PDF Question Answering System (RAG-powered)

[sample.pdf](https://github.com/user-attachments/files/25054686/sample.pdf)

> **Ask questions to your PDFs. Get precise, source-backed answers. Zero hallucinations.**

This project implements an **end-to-end Retrieval-Augmented Generation (RAG) pipeline** that allows users to upload a PDF, semantically understand its contents, and ask natural-language questions with **accurate, explainable answers grounded strictly in the document**.

Built with **BGM3 embeddings**, **semantic chunking**, and **cosine similarity search**, this system is lightweight, transparent, and production-ready — perfect for research papers, textbooks, technical manuals, and reports.

---

## ✨ Key Features

* 📘 **PDF → Knowledge Base**: Turn any PDF into a searchable intelligence layer
* 🧠 **Semantic Chunking**: Preserves context instead of naive splitting
* 🔢 **BGM3 Vector Embeddings**: High-quality multilingual embeddings
* 📐 **Cosine Similarity (scikit-learn)**: Fast & interpretable retrieval
* 🔍 **Source-Aware Answers**: Every response cites page & chunk references
* 🚫 **No Hallucinations**: LLM answers only from retrieved document context
* ⚡ **Simple & Modular Pipeline**: Easy to extend or swap components

---

## 🏗️ Architecture Overview (RAG)

This system follows a **classic but powerful RAG architecture**:

1. **Document Ingestion** – Read and validate PDFs
2. **Text Processing** – Extract, clean, normalize content
3. **Chunking Engine** – Create semantic chunks with metadata
4. **Embedding Generator** – Convert chunks into vector space
5. **Vector Store** – Persist embeddings + metadata
6. **Query Pipeline** – Embed user question & retrieve top matches
7. **LLM Reasoning Layer** – Generate grounded answers using Gemini

---

## 🔄 Step-by-Step Pipeline

```
read_pdf.py
    ↓
create_chunks.py
    ↓
embed_chunks.py
    ↓
query.py
```

Each stage is **decoupled**, making the system debuggable, extensible, and production-friendly.

---

## 🧩 Detailed Flow Explanation

### 1️⃣ User Input (PDF)

* User provides a PDF document
* Supported formats validated before processing

---

### 2️⃣ File Ingestion Layer (`read_pdf.py`)

* Reads PDF using **PyPDF**
* Extracts raw text from each page
* Handles malformed or scanned PDFs gracefully

---

### 3️⃣ Content Extraction

* Converts PDF pages into structured plain text
* Preserves page boundaries for traceability

---

### 4️⃣ Text Cleaning Layer

* Removes headers, footers, noise
* Normalizes whitespace and encoding
* Optional translation to English for consistency

---

### 5️⃣ Chunking Engine (`create_chunks.py`)

Instead of fixed-size splitting, the system creates **semantic chunks**:

* Maintains contextual meaning
* Attaches metadata:

  * `chunk_id`
  * `page_number`
  * `chunk_text`

This dramatically improves retrieval accuracy.

---

### 6️⃣ Embedding Generator (`embed_chunks.py`)

* Uses **BGM3 embedding model**
* Converts each chunk into a dense vector
* Saves:

  * `embeddings.json`
  * Corresponding metadata

These vectors form the **semantic memory** of the document.

---

### 7️⃣ Vector Store

* Lightweight JSON-based vector storage
* Includes:

  * Embedding vectors
  * Chunk text
  * Page & chunk references

Easily replaceable with FAISS / Pinecone / Weaviate later.

---

### 8️⃣ User Query (`query.py`)

* User asks a natural-language question
* Example:

  > *"What is the composition of white Portland cement?"*

---

### 9️⃣ Query Embedding

* Question is embedded using the **same BGM3 model**
* Ensures vector space consistency

---

### 🔟 Similarity Search

* Uses **Cosine Similarity (scikit-learn)**
* Compares query vector against all chunk embeddings
* Retrieves top-k most relevant chunks

---

### 1️⃣1️⃣ Context Builder

* Merges top-ranked chunks
* Builds a **strict prompt** for the LLM:

  * Answer only from provided context
  * Cite sources explicitly

---

### 1️⃣2️⃣ LLM Response Generator (Gemini API)

* Uses **Google Gemini**
* No external knowledge allowed
* Hallucination-free by design

---

### ✅ Final Answer Output

* Accurate
* Explainable
* Source-aware

---

## 🧪 Example Interaction

**User Question:**

> What is the composition of white Portland cement?

**System Answer:**

> White Portland cement is composed of dicalcium silicate (C2S, ~60%), tricalcium silicate (C3S, ~20–30%), and tricalcium aluminate (C3A, ~10%), along with the absence of iron oxide.

**References:**

* Page 18, Chunk 33

---

## 🛠️ Tech Stack

| Category      | Tools                                |
| ------------- | ------------------------------------ |
| Language      | Python 3.10+                         |
| LLM           | Google Gemini                        |
| Embeddings    | BGM3                                 |
| Vector Search | Cosine Similarity (scikit-learn)     |
| PDF Parsing   | PyPDF                                |
| Architecture  | Retrieval-Augmented Generation (RAG) |
| Utilities     | python-dotenv                        |


## 📌 Ideal Use Cases

* Research paper Q&A
* Legal / policy document analysis
* Technical manuals
* Educational material assistants
* Internal company knowledge bases

---

