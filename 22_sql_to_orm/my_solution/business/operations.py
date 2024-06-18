from datetime import datetime
from .interface import (
    DataStorageInterface,
    get_resource,
    get_all_resources,
    create_resource,
    delete_resource,
    FilterCondition,
    Operator
)
from .models import EventCreate, TicketCreate, EventReturn, TicketReturn
from .exceptions import OperationRejectedException
    

def get_event(dsi: DataStorageInterface, event_id: int) -> EventReturn:
    return get_resource(dsi, EventReturn, event_id)


def get_all_events(dsi: DataStorageInterface) -> list[EventReturn]:
    return get_all_resources(dsi, EventReturn)


def create_event(dsi: DataStorageInterface, event: EventCreate) -> EventReturn:
    return create_resource(dsi, event)


def delete_event(dsi: DataStorageInterface, event_id: int) -> EventReturn:
    with dsi:
        event = dsi.read(EventReturn, event_id)
        event_tickets = dsi.read_all(TicketReturn, FilterCondition("event_id", Operator.EQUALS, event_id))
        
        for ticket in event_tickets:
            dsi.delete(TicketReturn, ticket.id)
        
        dsi.delete(EventReturn, event_id)
        dsi.commit()
        return event



def get_ticket(dsi: DataStorageInterface, ticket_id: int) -> TicketReturn:
    return get_resource(dsi, TicketReturn, ticket_id)


def cancel_ticket(dsi: DataStorageInterface, ticket_id: int) -> TicketReturn:
    with dsi:
        ticket = dsi.read(TicketReturn, ticket_id)
        event = dsi.read(EventReturn, ticket.event_id)

        if event.has_started():
            raise OperationRejectedException("The event has already started")
        
        dsi.delete(TicketReturn, ticket_id)

        event.available_tickets += 1
        dsi.update(event)
        dsi.commit()

        return ticket
    

def change_name_on_ticket(dsi: DataStorageInterface, ticket_id: int, name: str) -> TicketReturn:
    with dsi:
        ticket = dsi.read(TicketReturn, ticket_id)
        event = dsi.read(EventReturn, ticket.event_id)

        if event.has_started():
            raise OperationRejectedException("The event has already started")
        
        ticket.customer_name = name
        dsi.update(ticket)
        dsi.commit()

        return ticket


def book_ticket(dsi: DataStorageInterface, ticket: TicketCreate) -> TicketReturn:
    with dsi:
        event = dsi.read(EventReturn, ticket.event_id)
        if event.available_tickets < 1:
            raise OperationRejectedException("No available tickets.")
        
        created_ticket = dsi.create(ticket)

        event.available_tickets -= 1
        dsi.update(event)
        dsi.commit()

        return created_ticket