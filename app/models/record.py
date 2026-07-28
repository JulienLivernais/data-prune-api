from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from app.core.database import Base
from typing import TYPE_CHECKING
import enum
from sqlalchemy import Enum as SAEnum
from sqlalchemy.dialects.postgresql import JSONB


if TYPE_CHECKING:
    from app.models.import_job import ImportJob


class RecordStatus(enum.Enum):
    accepted = "accepted"
    rejected = "rejected"


class Record(Base):
    __tablename__ = 'record'

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[dict] = mapped_column(JSONB, nullable=True)
    status: Mapped[RecordStatus] = mapped_column(SAEnum(RecordStatus), nullable=False)
    rejection_reason: Mapped[str | None] = mapped_column(String, nullable=True)

    import_job_id: Mapped[int] = mapped_column(ForeignKey("import_job.id"), nullable=False)
    import_job: Mapped["ImportJob"] = relationship(back_populates="records")



