import csv
import io
from fastapi import APIRouter, Depends, HTTPException
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


EXPORT_FIELDS_BY_SOURCE = {
    "un_comtrade": [
        "refYear", "reporterDesc", "partnerDesc", "flowDesc",
        "cmdCode", "cmdDesc", "primaryValue", "qty", "qtyUnitAbbr",
    ],
    "japan_customs": [
        "COMMODITY", "COUNTRY", "COUNTRY NAME", "UNIT1", "UNIT2",
        "CURRENT MONTH VALUE", "CUMULATIVE YEAR TO DATE VALUE",
    ],
}

SIGNATURE_KEY_BY_SOURCE = {
    "un_comtrade": "cmdCode",
    "japan_customs": "COMMODITY",
}


@router.get("/records/export")
def export_records(
    source: str,
    product: str | None = None,
    cmd_code: str | None = None,
    ref_year: int | None = None,
    db: Session = Depends(get_db),
):
    if source not in EXPORT_FIELDS_BY_SOURCE:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown source '{source}'. Expected one of: {list(EXPORT_FIELDS_BY_SOURCE.keys())}",
        )

    fields = EXPORT_FIELDS_BY_SOURCE[source]
    signature_key = SIGNATURE_KEY_BY_SOURCE[source]

    query = db.query(Record).filter(Record.status == RecordStatus.accepted)
    query = query.filter(Record.content.has_key(signature_key))

    if source == "un_comtrade":
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
    writer = csv.DictWriter(output, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    for record in records:
        writer.writerow(record.content)

    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=records_export_{source}.csv"},
    )