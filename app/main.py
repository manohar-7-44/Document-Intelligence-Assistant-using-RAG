from fastapi import FastAPI, HTTPException

from app.models import (
    QuestionRequest,
    QuestionResponse
)

from rag import (
    create_vector_store,
    ask_question
)

from app.database import (
    most_frequent_questions,
    unanswered_queries,
    average_latency
)

app = FastAPI(
    title="AWS Agreement RAG Assistant",
    description="""
    Retrieval-Augmented Generation (RAG) system built for the VeStaff AI Assignment.

    Features:
    - PDF Ingestion
    - FAISS Vector Search
    - Mistral LLM Question Answering
    - SQLite Analytics
    - FastAPI Backend
    """,
    version="1.0.0"
)

@app.post("/ingest")
def ingest_document():

    try:

        create_vector_store()

        return {
            "message":
            "Document ingested successfully"
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
@app.post(
    "/ask",
    response_model=QuestionResponse
)
def ask(
    request: QuestionRequest
):

    if not request.question.strip():

        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    try:

        result = ask_question(
            request.question
        )

        return QuestionResponse(
            answer=result["answer"],
            sources=result["sources"]
        )

    except FileNotFoundError:

        raise HTTPException(
            status_code=404,
            detail="Document not ingested yet"
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
@app.get("/analytics")
def analytics():

    return {

        "most_frequent_questions":
        most_frequent_questions(),

        "unanswered_queries":
        unanswered_queries(),

        "average_latency":
        average_latency()
    }

