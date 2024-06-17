from pydantic import BaseModel
from datetime import datetime


class EventCreate(BaseModel):
    title: str
    location: str
    start_date: datetime
    end_date: datetime
    available_tickets: int


class TicketCreate(BaseModel):
    event_id: int
    customer_name: str
    customer_email: str


class EventReturn(BaseModel):
    id: int | None
    title: str
    location: str
    start_date: datetime
    end_date: datetime
    available_tickets: int

    @classmethod
    def name(cls):
        return "Event"


class TicketReturn(BaseModel):
    id: int
    event_id: int
    customer_name: str
    customer_email: str

    @classmethod
    def name(cls):
        return "Ticket"