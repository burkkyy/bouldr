from datetime import datetime
from typing import Optional

from sqlalchemy import String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from src import db


class Boulder(db.Model):
    __tablename__ = "boulders"

    id: Mapped[int] = mapped_column("id", primary_key=True, autoincrement=True)

    author_id: Mapped[int] = mapped_column(
        "authorid",
        ForeignKey("users.id"),
        nullable=False,
    )

    region_id: Mapped[Optional[int]] = mapped_column(
        "regionid",
        ForeignKey("regions.id"),
        nullable=True,
    )

    name: Mapped[str] = mapped_column(String, nullable=False)

    description: Mapped[Optional[str]] = mapped_column(Text)

    image: Mapped[Optional[str]] = mapped_column(String)

    grade: Mapped[int] = mapped_column(nullable=False)

    coordinates: Mapped[Optional[str]] = mapped_column(String)

    created_at: Mapped[datetime] = mapped_column(
        "createdAt",
        DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        "updatedAt",
        DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )

    deleted_at: Mapped[Optional[datetime]] = mapped_column("deletedAt", DateTime)

    def __repr__(self):
        return f"<Boulder {self.name}>"