# RAG Settings
CHUNK_SIZE = 1500
CHUNK_OVERLAP = 300
TOP_K = 10

# Embedding Model
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Paths
PDF_PATH = "Data/AWS Customer Agreement.pdf"
VECTOR_DB_PATH = "vectorstore"

# Database
DATABASE_URL = "sqlite:///logs.db"