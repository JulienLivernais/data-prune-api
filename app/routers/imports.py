import hashlib
import uuid
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.import_job import ImportJob, SourceType
from app.schemas.import_job import ImportJobResponse
from worker.background_jobs import process_import

router = APIRouter()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

EXTENSION_TO_SOURCE_TYPE = {
    ".csv": SourceType.csv,
    ".xlsx": SourceType.excel,
    ".json": SourceType.json,
}


@router.post("/imports/files", response_model=ImportJobResponse)
def upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    extension = Path(file.filename).suffix.lower()
    source_type = EXTENSION_TO_SOURCE_TYPE.get(extension)

    if source_type is None:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {extension}")

    content = file.file.read()
    fingerprint = hashlib.sha256(content).hexdigest()

    existing_job = db.query(ImportJob).filter(ImportJob.fingerprint == fingerprint).first()
    if existing_job:
        raise HTTPException(status_code=409, detail="This file has already been processed")

    saved_filename = f"{uuid.uuid4()}{extension}"
    file_path = UPLOAD_DIR / saved_filename
    with open(file_path, "wb") as f:
        f.write(content)

    import_job = ImportJob(
        source_type=source_type,
        filename=file.filename,
        file_path=str(file_path),
        fingerprint=fingerprint,
    )
    db.add(import_job)
    db.commit()
    db.refresh(import_job)

    background_tasks.add_task(process_import, import_job.id)

    return import_job