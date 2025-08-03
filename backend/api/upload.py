import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.config.settings import UPLOAD_DIR
from backend.utils.file_utils import save_file
from backend.utils.status_utils import init_status_file, update_status
from backend.core.ingestion import ingest_file  # <-- NEW
from pathlib import Path

router = APIRouter()

# Initialize status.json file when the router is loaded
init_status_file()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    filename = os.path.basename(file.filename)
    file_ext = filename.split(".")[-1].lower()

    if file_ext not in ["pdf", "mp4"]:
        raise HTTPException(
            status_code=400, detail="Only PDF and MP4 files are supported."
        )

    file_path = UPLOAD_DIR / filename

    try:
        # Save file to disk
        save_file(file, file_path)

        # Update status to "processing"
        update_status(filename, "processing")

        # Ingest the file (e.g., extract text, chunk, and add to vector store)
        ingest_file(str(file_path), file_ext)

        # Update status to "done"
        update_status(filename, "done")

        return {
            "message": f"{filename} uploaded and processed successfully",
            "status": "done",
        }

    except Exception as e:
        # Update status to "failed" in case of any error
        update_status(filename, "failed")
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {str(e)}")
