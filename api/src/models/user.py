from datetime import datetime
from typing import Optional

from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from src import db

class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    username: Mapped[str] = mapped_column(String, nullable=False)

    display_name: Mapped[Optional[str]] = mapped_column(String)

    created_at: Mapped[datetime] = mapped_column(
        "createdAt",
        DateTime, 
        nullable=False, 
        server_default=func.current_timestamp()
    )

    updated_at: Mapped[datetime] = mapped_column(
        "updatedAt",
        DateTime, 
        nullable=False, 
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp()
    )

    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime)

    def __repr__(self):
        return f"<User {self.username}>"
