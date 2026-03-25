from datetime import datetime
from typing import Optional

from sqlalchemy import Float, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from src import db


class Send(db.Model):
    __tablename__ = "sends"

    id: Mapped[int] = mapped_column("id", primary_key=True, autoincrement=True)

    boulder_id: Mapped[int] = mapped_column(
        ForeignKey("boulders.id"),
        nullable=False,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    rating: Mapped[Optional[float]] = mapped_column(Float)

    send_type: Mapped[int] = mapped_column(nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )

    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime)

    def __repr__(self):
        return f"<Send {self.id}>"