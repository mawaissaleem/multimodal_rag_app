from fastapi import APIRouter, Query, HTTPException
from pathlib import Path
import json
import logging
from typing import Dict

# Logger setup
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Constants
STATUS_FILE = Path("status_store/status.json")

# Router setup
router = APIRouter(prefix="/status", tags=["Status"])


def load_status_data() -> Dict[str, str]:
    """
    Load the status data from the JSON file.

    Returns:
        A dictionary of filename -> status mappings.

    Raises:
        FileNotFoundError: If the status file does not exist.
        ValueError: If the file is not valid JSON.
    """
    if not STATUS_FILE.exists():
        logger.error("Missing status file at '%s'", STATUS_FILE)
        raise FileNotFoundError("status.json file is missing.")

    try:
        with STATUS_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
            logger.debug("Loaded status data: %s", data)
            return data
    except json.JSONDecodeError:
        logger.error("Invalid JSON format in '%s'", STATUS_FILE)
        raise ValueError("status.json is not a valid JSON file.")


@router.get("/")
def check_status(filename: str = Query(..., description="Name of the uploaded file")):
    """
    Check the current processing status of an uploaded file.

    Args:
        filename: Name of the uploaded file.

    Returns:
        A dictionary containing the filename and its status.

    Raises:
        HTTPException: If the status file is missing, invalid, or the filename is not found.
    """
    logger.info("Checking status for file: %s", filename)

    try:
        status_data = load_status_data()
    except (FileNotFoundError, ValueError) as e:
        logger.exception("Error loading status file.")
        raise HTTPException(status_code=500, detail=str(e))

    # Normalize file name
    filename = Path(filename).name

    if filename not in status_data:
        logger.warning("Status not found for file: %s", filename)
        raise HTTPException(
            status_code=404, detail=f"No status found for file '{filename}'"
        )

    logger.info("Status for '%s': %s", filename, status_data[filename])
    return {"filename": filename, "status": status_data[filename]}
