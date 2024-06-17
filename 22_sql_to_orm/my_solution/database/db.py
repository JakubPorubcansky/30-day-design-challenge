from __future__ import annotations
import business.models as md
import database.models as dbmd
from database.models import to_dict
from database.setup import DBSession

CREATE_TO_DB_TYPE_MAP = {
    md.EventCreate: dbmd.DBEvent,
    md.TicketCreate: dbmd.DBTicket
}

RETURN_TO_DB_TYPE_MAP = {
    md.EventReturn: dbmd.DBEvent,
    md.TicketReturn: dbmd.DBTicket
}

DB_TO_RETURN_TYPE_MAP = {value: key for key, value in RETURN_TO_DB_TYPE_MAP.items()}

class DataStorageHandler:
    def __init__(self):
        self.session = DBSession()

    def __enter__(self) -> DataStorageHandler:
        self.session.__enter__()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.__exit__(exc_type, exc_val, exc_tb)

    def commit(self):
        self.session.commit()

    def read[U](self, resource_type: type[U], resource_id: int) -> U | None:
        db_type = RETURN_TO_DB_TYPE_MAP[resource_type]
        db_resource = self.session.query(db_type).get(resource_id)
        if db_resource is None:
            return None
        return resource_type(**to_dict(db_resource))

    def read_all[U](self, resource_type: type[U]) -> list[U]:
        db_type = RETURN_TO_DB_TYPE_MAP[resource_type]
        db_resources = self.session.query(db_type).all()
        return [resource_type(**to_dict(db_resource)) for db_resource in db_resources]

    def create[T, U](self, resource: T) -> U:
        db_type = CREATE_TO_DB_TYPE_MAP[type(resource)]
        return_type = DB_TO_RETURN_TYPE_MAP[db_type]
        db_resource = db_type(**resource.dict())
        self.session.add(db_resource)
        self.session.flush()
        return return_type(**to_dict(db_resource))

    def update[U](self, resource: U) -> U | None:
        db_type = RETURN_TO_DB_TYPE_MAP[type(resource)]
        db_resource = self.session.query(db_type).get(resource.id)
        if db_resource is None:
            return None
        
        for key, value in resource.dict().items():
            setattr(db_resource, key, value)

        return resource

    def delete[U](self, resource_type: type[U], resource_id: int) -> U | None:
        db_type = RETURN_TO_DB_TYPE_MAP[resource_type]
        db_resource = self.session.query(db_type).get(resource_id)
        if db_resource is None:
            return None
        
        self.session.delete(db_resource)
        return resource_type(**to_dict(db_resource))