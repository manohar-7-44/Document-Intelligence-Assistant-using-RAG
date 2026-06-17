
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv
import os

load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

from app.config import (
    PDF_PATH,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    VECTOR_DB_PATH,
    TOP_K,
    EMBEDDING_MODEL
)

def load_pdf():
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()

    return documents

def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    chunks = splitter.split_documents(
        documents
    )

    return chunks

embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL
)

def create_vector_store():

    documents = load_pdf()

    chunks = split_documents(documents)

    vectorstore = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    vectorstore.save_local(
        VECTOR_DB_PATH
    )

    return vectorstore

def load_vector_store():

    vectorstore = FAISS.load_local(
        VECTOR_DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vectorstore

def get_retriever():

    vectorstore = load_vector_store()

    retriever = vectorstore.as_retriever(
        search_kwargs={"k": TOP_K}
    )

    return retriever

llm = ChatMistralAI(
    model="mistral-small-latest",
    api_key=MISTRAL_API_KEY,
    temperature=0
)

from app.database import log_query
import time

def ask_question(question):

    start_time = time.time()

    retriever = get_retriever()

    docs = retriever.invoke(question)

    context = ""
    
    if "summary" in question.lower():
        docs = load_pdf()

        context = ""

        for doc in docs:
            context += doc.page_content + "\n"

    for doc in docs:
        context += doc.page_content + "\n\n"

    prompt = f"""
You are an AWS Agreement assistant.

Answer the user's question using ONLY the provided context.

If the context partially answers the question,
provide the best possible answer.

Only say:

I could not find this information in the document.

if the context contains no relevant information at all.

Context:
{context}

Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)

    answer = response.content

    end_time = time.time()

    response_time = end_time - start_time

    log_query(
        question,
        answer,
        response_time
    )

    sources = []

    for doc in docs:
        sources.append(doc.page_content[:300])

    return {
        "answer": answer,
        "sources": sources
    }












