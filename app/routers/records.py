from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.record import Record
from app.schemas.record import RecordResponse

router = APIRouter()


@router.get("/records", response_model=list[RecordResponse])
def list_records(import_job_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(Record)

    if import_job_id is not None:
        query = query.filter(Record.import_job_id == import_job_id)

    return query.all()