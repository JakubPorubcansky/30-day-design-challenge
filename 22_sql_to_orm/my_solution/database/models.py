from typing import Any
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey


class Base(DeclarativeBase):
    pass


def to_dict(obj: Base | None) -> dict[str, Any]:
    if obj is None:
        return {}
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}


class DBEvent(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    location = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    available_tickets = Column(Integer)


class DBTicket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    customer_name = Column(String)
    customer_email = Column(String)
