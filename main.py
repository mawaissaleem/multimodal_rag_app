from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

sys.path.append(os.path.dirname(__file__))
# Import routers from backend
from backend.api import upload, query, status

app = FastAPI(
    title="Multimodal RAG API",
    version="1.0.0",
    description="Upload PDFs or videos, query documents, and check processing status.",
)

# Optional: CORS for local frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include endpoints
app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(query.router, prefix="/query", tags=["Query"])
app.include_router(status.router, prefix="/status", tags=["Status"])


@app.get("/")
def health_check():
    return {"message": "API is running"}
