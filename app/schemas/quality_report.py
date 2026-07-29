from pydantic import BaseModel, ConfigDict


class QualityReportBase(BaseModel):
    pass


class QualityReportResponse(QualityReportBase):
    id: int
    input_records: int
    rejected_records: int
    values_corrected: int
    duplicates_removed: int
    import_job_id: int

    model_config = ConfigDict(from_attributes=True)

