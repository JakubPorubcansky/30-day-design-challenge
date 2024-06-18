from typing import Annotated    
from fastapi import APIRouter, Depends, Body
import business.operations as operations
import business.models as md
from database.db import DatabaseHandler

router = APIRouter()

def get_db_handler():
    handler = DatabaseHandler()
    yield handler

@router.post("/events", response_model=md.EventReturn)
async def create_event(event: md.EventCreate, handler = Depends(get_db_handler)):
    return operations.create_event(handler, event)


@router.delete("/events/{event_id}", response_model=md.EventReturn)
async def delete_event(event_id: int, handler = Depends(get_db_handler)):
    return operations.delete_event(handler, event_id)


@router.get("/events/{event_id}", response_model=md.EventReturn)
async def get_event(event_id: int, handler = Depends(get_db_handler)):
    return operations.get_event(handler, event_id)


@router.get("/events", response_model=list[md.EventReturn])
async def get_all_events(handler = Depends(get_db_handler)):
    return operations.get_all_events(handler)


@router.post("/tickets", response_model=md.TicketReturn)
async def book_ticket(ticket: md.TicketCreate, handler = Depends(get_db_handler)):
    return operations.book_ticket(handler, ticket)


@router.patch("/tickets/{ticket_id}", response_model=md.TicketReturn)
async def change_customer_name_on_ticket(ticket_id: int, customer_name: Annotated[str, Body(embed=True)], handler = Depends(get_db_handler)):
    return operations.change_name_on_ticket(handler, ticket_id, customer_name)


@router.get("/tickets/{ticket_id}", response_model=md.TicketReturn)
async def get_ticket(ticket_id: int, handler = Depends(get_db_handler)):
    return operations.get_ticket(handler, ticket_id)


@router.delete("/tickets/{ticket_id}", response_model=md.TicketReturn)
async def cancel_ticket(ticket_id: int, handler = Depends(get_db_handler)):
    return operations.cancel_ticket(handler, ticket_id)