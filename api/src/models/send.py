from datetime import datetime
from typing import Optional

from sqlalchemy import Float, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from src import db


class Send(db.Model):
    __tablename__ = "sends"

    id: Mapped[int] = mapped_column("id", primary_key=True, autoincrement=True)

    boulder_id: Mapped[int] = mapped_column(
        "boulderid",
        ForeignKey("boulders.id"),
        nullable=False,
    )

    user_id: Mapped[int] = mapped_column(
        "userid",
        ForeignKey("users.id"),
        nullable=False,
    )

    rating: Mapped[Optional[float]] = mapped_column(Float)

    send_type: Mapped[int] = mapped_column("sendType", nullable=False)

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
        return f"<Send {self.id}>"