from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.import_job import ImportJob, Status
from app.models.quality_report import QualityReport
from app.schemas.quality_report import QualityReportResponse

router = APIRouter()


@router.get("/reports/{import_job_id}")
def get_report(import_job_id: int, db: Session = Depends(get_db)):
    import_job = db.query(ImportJob).filter(ImportJob.id == import_job_id).first()

    if import_job is None:
        raise HTTPException(status_code=404, detail="Import job not found")

    if import_job.status in (Status.pending, Status.processing):
        return JSONResponse(status_code=202, content={"status": "processing"})

    if import_job.status == Status.failed:
        raise HTTPException(status_code=500, detail="Import processing failed")

    quality_report = db.query(QualityReport).filter(
        QualityReport.import_job_id == import_job_id
    ).first()

    return QualityReportResponse.model_validate(quality_report)

