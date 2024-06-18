import requests

API_URL = "http://localhost:8000"


def get_new_event():
    event_data = {
        "title": "Python Conference 2025",
        "location": "Amsterdam",
        "start_date": "2025-03-15 09:00:00",
        "end_date": "2025-03-18 16:00:00",
        "available_tickets": 50,
    }
    return event_data


def get_past_event():
    event_data = {
        "title": "Python Conference 2020",
        "location": "Amsterdam",
        "start_date": "2020-03-15 09:00:00",
        "end_date": "2020-03-18 16:00:00",
        "available_tickets": 50,
    }
    return event_data


def create_event(event_data: dict) -> dict | None:
    response = requests.post(f"{API_URL}/events", json=event_data, timeout=5)

    if response.status_code == 200:
        print(f"Event created successfully: {response.json()}")
        return response.json()
    else:
        print(f"Error creating event: {response.content}")
        return None


def get_all_events() -> dict | None:
    response = requests.get(f"{API_URL}/events", timeout=5)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error getting all events: {response.content}")
        return None


def book_ticket(event_id: int) -> dict | None:
    ticket_data = {
        "event_id": event_id,
        "customer_name": "Jon Doe",
        "customer_email": "test@example.com",
    }

    response = requests.post(f"{API_URL}/tickets", json=ticket_data, timeout=5)

    if response.status_code == 200:
        print(f"Ticket booked successfully for event with id {event_id}")
        return response.json()
    else:
        print(f"Error booking ticket for event with id {event_id}: {response.content}")
        return None


def change_customer_name_on_ticket(ticket_id: int, customer_name: str) -> dict | None:
    url = f"{API_URL}/tickets/{ticket_id}"
    response = requests.patch(url, json={"customer_name": customer_name}, timeout=5)
    
    if response.status_code == 200:
        print(f"Name on ticket with id {ticket_id} changed to {customer_name}.")
        return response.json()
    else:
        print(f"Error changing name on ticket with id {ticket_id}: {response.content}")
        return None


def cancel_ticket(ticket_id: int):
    url = f"{API_URL}/tickets/{ticket_id}"
    response = requests.delete(url, timeout=5)
    if response.status_code == 200:
        print(f"Ticket with id {ticket_id} deleted successfully.")
    else:
        print(f"Error deleting ticket with id {ticket_id}: {response.content}")



def delete_event(event_id: int):
    # Delete an event from the database
    url = f"{API_URL}/events/{event_id}"
    response = requests.delete(url, timeout=5)
    if response.status_code == 200:
        print(f"Event with id {event_id} deleted successfully.")
    else:
        print(f"Error deleting event with id {event_id}: {response.content}")


def main():
    all_events_0 = get_all_events()
    
    for event in all_events_0:
        delete_event(event["id"])

    past_event = create_event(event_data=get_past_event())
    new_event = create_event(event_data=get_new_event())

    all_events_1 = get_all_events()

    book_ticket(event_id=past_event["id"])
    ticket_1 = book_ticket(event_id=new_event["id"])
    ticket_2 = book_ticket(event_id=new_event["id"])

    ticket_1_changed = change_customer_name_on_ticket(ticket_id=ticket_1["id"], customer_name="Kubco Porubco")
    cancel_ticket(ticket_id=ticket_2["id"])

    delete_event(event_id=2)

    all_events_2 = get_all_events()


if __name__ == "__main__":
    main()
