# AWS Agreement RAG Assistant

## Project Overview

This project is a Retrieval-Augmented Generation (RAG) system built for the VeStaff Junior AI Developer Assignments.

The application enables users to ask questions about the AWS Customer Agreement and receive context-aware answers grounded in the document content. It combines document retrieval, semantic search, large language models, SQL logging, and analytics.

## Features

### Document Processing
- PDF document ingestion
- Recursive text chunking
- Embedding generation
- FAISS vector database creation

### Question Answering
- Retrieval-Augmented Generation (RAG)
- Semantic similarity search
- Mistral AI integration
- Source chunk retrieval

### Logging & Analytics
- SQLite database logging
- Question tracking
- Answer tracking
- Response latency tracking
- Timestamp logging

### Analytics Dashboard
- Most frequently asked questions
- Queries where no answer was found
- Average response latency

### Frontend
- Streamlit user interface
- Question & answer history
- Source viewing
- Analytics display

## Tech Stack

### Backend
- Python
- FastAPI

### RAG Components
- LangChain
- FAISS
- Sentence Transformers
- Mistral AI

### Database
- SQLite

### Frontend
- Streamlit

### Embedding Model
- sentence-transformers/all-MiniLM-L6-v2

### Language Model
- mistral-small-latest

## Project Structure

```text
VeStaff_RAG_Assignment/

app/
|--> __init__.py
|--> config.py
|--> database.py
|--> main.py
|--> models.py

Frontend/
|--> streamlit_app.py

Data/
|--> AWS Customer Agreement.pdf

vectorstore/
|--> index.faiss
|--> index.pkl

rag.py
logs.db
.env
.gitignore
requirement.txt
README.md
```

## Installation

### Clone Repository

```bash
git clone https://github.com/pardhiva23/VeStaff_RAG_Assignment.git
cd VeStaff_RAG_Assignment
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

#### Windows

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirement.txt
```

## Environment Variables

Create a `.env` file in the project root:

```env
MISTRAL_API_KEY=your_mistral_api_key
```

## Running the Application

### Start FastAPI Backend

- Run This in the Terminal-1

```bash
uvicorn app.main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

---

### Start Streamlit Frontend

- Run This in the Terminal-2 and don't close the Terminal-1 (Both must be running)

```bash
streamlit run Frontend/streamlit_app.py
```

Frontend URL:

```text
http://localhost:8501
```

## API Endpoints

### POST /ingest

Processes the PDF document and creates the FAISS vector store.

Response:

```json
{
  "message": "Document ingested successfully"
}
```

---

### POST /ask

Request:

```json
{
  "question": "What happens after termination?"
}
```

Response:

```json
{
  "answer": "After termination of the AWS Customer Agreement...",
  "sources": [(b) Termination for Cause...]
}
```

---

### GET /analytics

Response:

```json
{
  "most_frequent_questions": [["What happens after termination?",3],...],
  "unanswered_queries": [["Who won IPL 2025?"],...],
  "average_latency": It is the average time your system takes to answer a user's question.
}
```

## Architecture Overview

The system follows a Retrieval-Augmented Generation (RAG) architecture.

## Architecture

```text
AWS Agreement PDF
        |
        v
PyPDFLoader
        |
        v
Text Chunking
(RecursiveCharacterTextSplitter)
        |
        v
Embeddings
(all-MiniLM-L6-v2)
        |
        v
FAISS Vector Store
        |
        v
Retriever
        |
        v
Mistral AI
        |
        v
Answer Generation
        |
        v
SQLite Logging
        |
        v
Analytics
```

### Workflow

1. The AWS Customer Agreement PDF is loaded using PyPDFLoader.
2. The document is split into smaller chunks using RecursiveCharacterTextSplitter.
3. Each chunk is converted into vector embeddings using the Sentence Transformers embedding model.
4. The embeddings are stored in a FAISS vector database.
5. When a user submits a question:
   - The question is converted into an embedding.
   - FAISS retrieves the most relevant document chunks.
   - Retrieved chunks are combined into a context.
   - The context and question are sent to Mistral AI.
6. The generated answer is returned along with the retrieved source chunks.
7. Every interaction is logged into SQLite for analytics.
8. Analytics are exposed through a FastAPI endpoint and visualized in Streamlit.

### System Components

```text
1.Frontend (Streamlit)
2.FastAPI Backend
3.RAG Pipeline
4.FAISS Vector Store
5.Mistral AI
6.SQLite Logging & Analytics
```

## Key Design Decisions and Assumptions

### Chunking Strategy

The document is split using RecursiveCharacterTextSplitter.

Configuration:

```python
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
```

Reasoning:

- Smaller chunks improve retrieval precision.
- Overlap preserves context across chunk boundaries.
- RecursiveCharacterTextSplitter works effectively for legal documents.

---

### Embedding Model

Model Used:

```text
sentence-transformers/all-MiniLM-L6-v2
```

Reasoning:

- Lightweight and efficient.
- Strong semantic retrieval performance.
- Free and locally deployable.
- Suitable for assignment-scale RAG systems.

---

### Vector Database

FAISS was selected because:

- Fast similarity search.
- Lightweight local deployment.
- No external database requirements.
- Seamless integration with LangChain.

---

### LLM Choice

Model:

```text
mistral-small-latest
```

Provider:

```text
Mistral AI
```

Reasoning:

- Strong instruction-following capabilities.
- Fast inference.
- Good balance between quality and cost.
- Suitable for RAG-based applications.

---

### Retrieval Strategy

Configuration:

```python
TOP_K = 5
```

Reasoning:

- Retrieves the five most relevant chunks.
- Provides sufficient context for answer generation.
- Reduces irrelevant information passed to the model.

---

### Logging Design

A SQLite database is used to store:

- User question
- Generated answer
- Response latency
- Timestamp

Reasoning:

- Lightweight and easy to deploy.
- Satisfies assignment requirements.
- Enables efficient analytics generation.

### Analytics Implemented

The following SQL-based analytics are provided:

1. Most Frequently Asked Questions
2. Queries Where No Answer Was Found
3. Average Response Latency

These analytics are computed using SQL aggregation operations such as:

- COUNT()
- GROUP BY
- AVG()

## Testing

The system was tested using:

### In-Scope Questions

- What happens after termination?
- What are AWS payment obligations?
- When can AWS suspend services?
- What is AWS liability?

### Out-of-Scope Questions

- Who won IPL 2025?
- What is Messi's age?

These queries were logged and used for analytics generation.

## Assumptions

- The system processes a single PDF document.
- Users ask questions related to the AWS Customer Agreement.
- A valid Mistral API key is available through environment variables.
- Internet access is available for LLM inference.
- Analytics are generated from interactions stored in SQLite.
