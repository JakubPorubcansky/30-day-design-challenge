from functools import wraps
from .interface import (
    DataStorageInterface,
    get_resource,
    get_all_resources,
    create_resource,
    delete_resource,
    FilterCondition,
    Operator
)
from .config import Config
from .notifications.core import trigger_event, NotificationTrigger
from .models import EventCreate, TicketCreate, EventReturn, TicketReturn
from .exceptions import OperationRejectedException
    

def with_data_storage(func):
    @wraps(func)
    def wrapper(dsi: DataStorageInterface, *args, **kwargs):
        with dsi:
            return func(dsi, *args, **kwargs)
        
    return wrapper


@with_data_storage
def get_event(dsi: DataStorageInterface, event_id: int) -> EventReturn:
    return get_resource(dsi, EventReturn, event_id)


@with_data_storage
def get_all_events(dsi: DataStorageInterface) -> list[EventReturn]:
    return get_all_resources(dsi, EventReturn)


@with_data_storage
def create_event(dsi: DataStorageInterface, event: EventCreate) -> EventReturn:
    created_event = create_resource(dsi, event)
    dsi.commit()

    if Config.SEND_NOTIFICATIONS:
        trigger_event(NotificationTrigger.EVENT_CREATED, event=created_event)

    return created_event


@with_data_storage
def delete_event(dsi: DataStorageInterface, event_id: int) -> EventReturn:
    event = get_resource(dsi, EventReturn, event_id)
    event_tickets = dsi.read_all(TicketReturn, FilterCondition("event_id", Operator.EQUALS, event_id))
    
    for ticket in event_tickets:
        dsi.delete(TicketReturn, ticket.id)
    
    dsi.delete(EventReturn, event_id)
    dsi.commit()
    return event


@with_data_storage
def get_ticket(dsi: DataStorageInterface, ticket_id: int) -> TicketReturn:
    return get_resource(dsi, TicketReturn, ticket_id)


@with_data_storage
def cancel_ticket(dsi: DataStorageInterface, ticket_id: int) -> TicketReturn:
    ticket = get_resource(dsi, TicketReturn, ticket_id)
    event = get_resource(dsi, EventReturn, ticket.event_id)

    if event.has_started():
        raise OperationRejectedException("The event has already started")
    
    dsi.delete(TicketReturn, ticket_id)

    event.available_tickets += 1
    dsi.update(event)
    dsi.commit()

    return ticket
    

@with_data_storage
def change_name_on_ticket(dsi: DataStorageInterface, ticket_id: int, name: str) -> TicketReturn:
    ticket = get_resource(dsi, TicketReturn, ticket_id)
    event = get_resource(dsi, EventReturn, ticket.event_id)

    if event.has_started():
        raise OperationRejectedException("The event has already started")
    
    ticket.customer_name = name
    dsi.update(ticket)
    dsi.commit()

    return ticket


@with_data_storage
def book_ticket(dsi: DataStorageInterface, ticket: TicketCreate) -> TicketReturn:
    event = get_resource(dsi, EventReturn, ticket.event_id)
    
    if not event.tickets_available():
        raise OperationRejectedException("No available tickets.")
    
    if event.has_started():
        raise OperationRejectedException("The event has already started")
    
    created_ticket = dsi.create(ticket)

    event.available_tickets -= 1
    dsi.update(event)
    dsi.commit()
    
    if Config.SEND_NOTIFICATIONS:
        trigger_event(NotificationTrigger.TICKET_BOOKED, ticket=created_ticket)

    return created_ticket