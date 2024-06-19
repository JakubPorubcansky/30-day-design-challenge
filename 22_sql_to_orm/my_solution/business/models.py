from typing import Self
from pydantic import BaseModel, NonNegativeInt, EmailStr, model_validator
from datetime import datetime


class EventCreate(BaseModel):
    title: str
    location: str
    start_date: datetime
    end_date: datetime
    available_tickets: NonNegativeInt

    @model_validator(mode='after')
    def check_passwords_match(self) -> Self:
        if self.start_date >= self.end_date:
            raise ValueError('start_date has to be before end_date')
        return self


class TicketCreate(BaseModel):
    event_id: int
    customer_name: str
    customer_email: EmailStr


class EventReturn(BaseModel):
    id: int | None
    title: str
    location: str
    start_date: datetime
    end_date: datetime
    available_tickets: NonNegativeInt

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
    customer_email: EmailStr

    @classmethod
    def name(cls):
        return "Ticket"