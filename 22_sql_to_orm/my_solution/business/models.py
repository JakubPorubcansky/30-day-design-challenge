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
    
    def has_started(self) -> bool:
        return datetime.now() >= self.start_date

    def has_finished(self) -> bool:
        return datetime.now() > self.end_date

    def tickets_available(self) -> bool:
        return self.available_tickets > 0


class TicketReturn(BaseModel):
    id: int
    event_id: int
    customer_name: str
    customer_email: str

    @classmethod
    def name(cls):
        return "Ticket"