from fastapi import APIRouter
import business.operations as operations
import business.models as models
from database.db import DataStorageHandler

router = APIRouter()


@router.post("/events")
async def create_event(event: models.EventCreate):
    handler = DataStorageHandler()
    event = operations.create_event(handler, event)
    return {"event_id": event.id}


@router.delete("/events/{event_id}")
async def delete_event(event_id: int):
    handler = DataStorageHandler()
    event = operations.delete_event(handler, event_id)
    return dict(event)


@router.get("/events/{event_id}")
async def get_event(event_id: int):
    handler = DataStorageHandler()
    event = operations.get_event(handler, event_id)
    return dict(event)


@router.get("/events")
async def get_all_events():
    handler = DataStorageHandler()
    events = operations.get_all_events(handler)
    return [dict(event) for event in events]


@router.post("/tickets")
async def book_ticket(ticket: models.TicketCreate):
    handler = DataStorageHandler()
    ticket = operations.book_ticket(handler, ticket)
    return {"ticket_id": ticket.id}


@router.get("/tickets/{ticket_id}")
async def get_ticket(ticket_id: int):
    handler = DataStorageHandler()
    ticket = operations.get_ticket(handler, ticket_id)
    return dict(ticket)
