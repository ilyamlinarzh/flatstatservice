from src.db import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, DateTime, Index
from datetime import datetime


class Results(Base):
    __tablename__ = 'results'

    id_: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    ip: Mapped[str]
    city: Mapped[str]
    result: Mapped[str]
    datetime: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    __table_args__ = (
        Index('idx_city', 'city'),
        Index('idx_city_result', 'city', 'result')
    )
