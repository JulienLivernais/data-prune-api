from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey
from app.core.database import Base
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.models.import_job import ImportJob


class QualityReport(Base):
    __tablename__ = 'quality_report'

    id: Mapped[int] = mapped_column(primary_key=True)

    input_records: Mapped[int] = mapped_column(Integer, nullable=False)
    rejected_records: Mapped[int] = mapped_column(Integer, nullable=False)
    values_corrected: Mapped[int] = mapped_column(Integer, nullable=False)
    duplicates_removed: Mapped[int] = mapped_column(Integer, nullable=False)

    import_job_id: Mapped[int] = mapped_column(
        ForeignKey("import_job.id"), nullable=False, unique=True
    )
    import_job: Mapped["ImportJob"] = relationship(back_populates="quality_report")

