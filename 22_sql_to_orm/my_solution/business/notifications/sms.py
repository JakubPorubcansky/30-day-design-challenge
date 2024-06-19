from .core import subscribe_handler, NotificationTrigger, NotificationContext


def ticket_booked_sms_notification_handler(ctx: NotificationContext):
    print(f"SMS: Your ticket has been reserved under id {ctx.ticket.id} on name {ctx.ticket.customer_name}!")


def subscribe():
    subscribe_handler(NotificationTrigger.TICKET_BOOKED, ticket_booked_sms_notification_handler)