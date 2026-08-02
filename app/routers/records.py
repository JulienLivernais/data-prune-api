import csv
import io
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import cast, String
from app.core.database import get_db
from app.models.record import Record, RecordStatus
from app.schemas.record import RecordResponse


router = APIRouter()


@router.get("/records", response_model=list[RecordResponse])
def list_records(import_job_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(Record)

    if import_job_id is not None:
        query = query.filter(Record.import_job_id == import_job_id)

    return query.all()


EXPORT_FIELDS = [
    "refYear", "reporterDesc", "partnerDesc", "flowDesc",
    "cmdCode", "cmdDesc", "primaryValue", "qty", "qtyUnitAbbr",
]


@router.get("/records/export")
def export_records(
    product: str | None = None,
    cmd_code: str | None = None,
    ref_year: int | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Record).filter(Record.status == RecordStatus.accepted)

    if product is not None:
        query = query.filter(
            cast(Record.content["cmdDesc"], String).ilike(f'%{product}%')
        )

    if cmd_code is not None:
        query = query.filter(
            cast(Record.content["cmdCode"], String) == cmd_code
        )

    if ref_year is not None:
        query = query.filter(
            cast(Record.content["refYear"], String) == str(ref_year)
        )

    records = query.all()

    output = io.StringIO()

    writer = csv.DictWriter(output, fieldnames=EXPORT_FIELDS, extrasaction="ignore")
    writer.writeheader()
    for record in records:
        writer.writerow(record.content)

    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=records_export.csv"},
    )