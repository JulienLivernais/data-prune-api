from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text
from app.core.database import Base
from datetime import datetime, timezone
from sqlalchemy import DateTime
import enum
from sqlalchemy import Enum as SAEnum
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.models.record import Record
    from app.models.quality_report import QualityReport


class SourceType(enum.Enum):
    csv = "csv"
    excel = "excel"
    json = "json"


class Status(enum.Enum):
    pending="pending"
    processing="processing"
    finished="finished"
    failed="failed"


class ImportJob (Base):
    __tablename__ = 'import_job'

    id: Mapped[int] = mapped_column(primary_key=True)
    source_type: Mapped[SourceType] = mapped_column(SAEnum(SourceType), nullable=False)
    filename: Mapped[str] = mapped_column(String, nullable=True)
    file_path: Mapped[str] = mapped_column(String, nullable=True)
    fingerprint: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    status: Mapped[Status] = mapped_column(SAEnum(Status), nullable=False, default=Status.pending)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    records: Mapped[list["Record"]] = relationship(
        back_populates="import_job",
        cascade="all, delete, delete-orphan",
    )

    quality_report: Mapped["QualityReport"] = relationship(
        back_populates="import_job",
        uselist=False,
        cascade="all, delete, delete-orphan",
    )



