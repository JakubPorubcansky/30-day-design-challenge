from fastapi.testclient import TestClient
from main import app
from api.routes import get_db_handler
from business.models import EventReturn

class TestDatabaseHandler:
    def __init__(self):
        self.n_commits = 0
        self.n_creates = 0

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def commit(self):
        self.n_commits += 1

    def create[T, U](self, resource: T) -> U:
        self.n_creates += 1
        return EventReturn(id=100, **resource.dict())


client = TestClient(app)

def test_create_event():
    handler = TestDatabaseHandler()
    app.dependency_overrides[get_db_handler] = lambda: handler
    test_event = {
        "title": "Python Conference 2023",
        "location": "Amsterdam",
        "start_date": "2023-03-15 09:00:00",
        "end_date": "2023-03-18 16:00:00",
        "available_tickets": 50,
    }

    response = client.post("/events", json=test_event)

    assert response.status_code == 200
    assert handler.n_creates == 1
    assert handler.n_commits == 1


if __name__ == "__main__":
    test_create_event()
