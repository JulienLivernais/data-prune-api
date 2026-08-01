from datetime import datetime, timezone
from app.core.database import SessionLocal
from app.models.import_job import ImportJob, Status
from app.models.record import Record, RecordStatus
from app.models.quality_report import QualityReport
from importers.distributor import get_importer
from pipeline.pipeline import run_pipeline


def process_import(import_job_id: int) -> None:
    db = SessionLocal()

    try:
        import_job = db.query(ImportJob).filter(ImportJob.id == import_job_id).first()

        import_job.status = Status.processing
        db.commit()

        importer = get_importer(import_job.source_type.value)
        raw_records = importer.extract(import_job.file_path)

        valid_records, rejected_records, values_corrected, duplicates_removed = run_pipeline(raw_records)

        for row in valid_records:
            db.add(Record(
                content=row,
                status=RecordStatus.accepted,
                rejection_reason=None,
                import_job_id=import_job.id,
            ))

        for item in rejected_records:
            db.add(Record(
                content=item["content"],
                status=RecordStatus.rejected,
                rejection_reason=item["rejection_reason"],
                import_job_id=import_job.id,
            ))

        db.add(QualityReport(
            input_records=len(raw_records),
            rejected_records=len(rejected_records),
            values_corrected=values_corrected,
            duplicates_removed=duplicates_removed,
            import_job_id=import_job.id,
        ))

        import_job.status = Status.finished
        import_job.completed_at = datetime.now(timezone.utc)
        db.commit()

    except Exception:
        import_job.status = Status.failed
        db.commit()
        raise

    finally:
        db.close()