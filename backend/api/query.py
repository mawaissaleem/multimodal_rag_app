from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from backend.api.query_services import semantic_search
from backend.api.gpt_generator import GPT2Generator

router = APIRouter()

# Initialize GPT model once at startup
gpt_generator = GPT2Generator()


class QueryRequest(BaseModel):
    question: str
    filename: Optional[str] = None
    top_k: Optional[int] = 5


class QueryResponse(BaseModel):
    question: str
    results: List[str]
    generated_answer: str


@router.post("/query", response_model=QueryResponse)
def query_documents(request: QueryRequest):
    try:
        documents = semantic_search(
            query=request.question, filename=request.filename, top_k=request.top_k
        )

        # Join top-k documents into a single string context for GPT2
        context = "\n".join(documents).strip()

        if not context:
            raise ValueError("No documents found for the given query.")

        # Generate a meaningful answer
        generated = gpt_generator.generate_summary(context)

        return QueryResponse(
            question=request.question, results=documents, generated_answer=generated
        )

    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
