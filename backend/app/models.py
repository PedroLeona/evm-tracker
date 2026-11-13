"""SQLAlchemy models. Must stay in sync with db/01_init.sql."""

from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.constants import (
    DECIMAL_PLACES,
    DESCRIPTION_MAX_LENGTH,
    MONEY_MAX_DIGITS,
    NAME_MAX_LENGTH,
    PERCENT_MAX_DIGITS,
)
from app.database import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(NAME_MAX_LENGTH))
    description: Mapped[str | None] = mapped_column(String(DESCRIPTION_MAX_LENGTH))

    activities: Mapped[list["Activity"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
        order_by="Activity.id",
    )


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), index=True
    )
    name: Mapped[str] = mapped_column(String(NAME_MAX_LENGTH))
    budget_at_completion: Mapped[Decimal] = mapped_column(
        Numeric(MONEY_MAX_DIGITS, DECIMAL_PLACES)
    )
    planned_percent: Mapped[Decimal] = mapped_column(
        Numeric(PERCENT_MAX_DIGITS, DECIMAL_PLACES)
    )
    actual_percent: Mapped[Decimal] = mapped_column(
        Numeric(PERCENT_MAX_DIGITS, DECIMAL_PLACES)
    )
    actual_cost: Mapped[Decimal] = mapped_column(
        Numeric(MONEY_MAX_DIGITS, DECIMAL_PLACES)
    )

    project: Mapped[Project] = relationship(back_populates="activities")
