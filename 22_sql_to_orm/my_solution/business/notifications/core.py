from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional
from ..models import TicketReturn, EventReturn


@dataclass
class NotificationContext():
    event: Optional[EventReturn] = None
    ticket: Optional[TicketReturn] = None


class NotificationTrigger(Enum):
    TICKET_BOOKED = auto()
    EVENT_CREATED = auto()


NotificationHandler = Callable[[NotificationContext], None]

subscriptions: Dict[NotificationTrigger, List[NotificationHandler]] = {}


def subscribe_handler(trigger: NotificationTrigger, handler: NotificationHandler) -> None:
    if not trigger in subscriptions:
        subscriptions[trigger] = []
    
    subscriptions[trigger].append(handler)


def trigger_event(trigger: NotificationTrigger, **kwargs) -> None:
    context = NotificationContext(**kwargs)
    for handler in subscriptions[trigger]:
        handler(context)