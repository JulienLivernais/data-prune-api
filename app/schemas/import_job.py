from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.models.import_job import SourceType, Status


class ImportJobBase(BaseModel):
    pass


class ImportJobResponse(ImportJobBase):
    id: int
    source_type: SourceType
    filename: str | None
    status: Status
    created_at: datetime
    completed_at: datetime | None

    model_config = ConfigDict(from_attributes=True)



