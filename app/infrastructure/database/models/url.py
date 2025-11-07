from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from infrastructure.database.models.base import TimedBaseModel


class URLModel(TimedBaseModel):
    __tablename__ = "url"

    long_url: Mapped[str] = mapped_column(String(2048), nullable=False)
    short_url: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
