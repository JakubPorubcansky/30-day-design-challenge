from .interface import (
    DataStorageInterface,
    get_resource,
    get_all_resources,
    create_resource,
    delete_resource,
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
    return delete_resource(dsi, EventReturn, event_id)


def get_ticket(dsi: DataStorageInterface, ticket_id: int) -> TicketReturn:
    return get_resource(dsi, TicketReturn, ticket_id)


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