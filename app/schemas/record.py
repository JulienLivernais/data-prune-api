from pydantic import BaseModel, ConfigDict
import enum


class RecordStatus(str, enum.Enum):
    accepted = "accepted"
    rejected = "rejected"


class RecordBase(BaseModel):
    pass


class RecordResponse(RecordBase):
    id: int
    content: dict | None
    status: RecordStatus
    rejection_reason: str | None
    import_job_id: int

    model_config = ConfigDict(from_attributes=True)

