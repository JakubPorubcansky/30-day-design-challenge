from .core import subscribe_handler, NotificationTrigger, NotificationContext


def ticket_booked_email_notification_handler(ctx: NotificationContext):
    print(f"Email: Your ticket has been reserved under id {ctx.ticket.id} on name {ctx.ticket.customer_name}!")


def event_created_email_notification_handler(ctx: NotificationContext):
    print(f"Email: New event! \"{ctx.event.title}\" will be held in {ctx.event.location} from {ctx.event.start_date} to {ctx.event.end_date}.")


def subscribe():
    subscribe_handler(NotificationTrigger.TICKET_BOOKED, ticket_booked_email_notification_handler)
    subscribe_handler(NotificationTrigger.EVENT_CREATED, event_created_email_notification_handler)