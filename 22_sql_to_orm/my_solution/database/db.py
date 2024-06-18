from __future__ import annotations
from typing import Any, Optional
from sqlalchemy import or_, and_
import business.models as md
from business.interface import (
    Condition, 
    FilterCondition, 
    JointCondition, 
    Operator,
    ConditionsJoinOperator
)
import database.models as dbmd
from database.models import to_dict
from database.setup import DBSession

CONDITION_TO_SQLALCHEMY_OPERATOR_MAP = {
    Operator.EQUALS: lambda attribute, value: attribute == value,
    Operator.NOT_EQUALS: lambda attribute, value: attribute != value,
    Operator.LESS_THAN: lambda attribute, value: attribute < value,
    Operator.LESS_THAN_OR_EQUAL: lambda attribute, value: attribute <= value,
    Operator.GREATER_THAN: lambda attribute, value: attribute > value,
    Operator.GREATER_THAN_OR_EQUAL: lambda attribute, value: attribute >= value,
}

CREATE_TO_DB_TYPE_MAP = {
    md.EventCreate: dbmd.DBEvent,
    md.TicketCreate: dbmd.DBTicket
}

RETURN_TO_DB_TYPE_MAP = {
    md.EventReturn: dbmd.DBEvent,
    md.TicketReturn: dbmd.DBTicket
}

DB_TO_RETURN_TYPE_MAP = {value: key for key, value in RETURN_TO_DB_TYPE_MAP.items()}

class DatabaseHandler:
    def __init__(self):
        self.session = DBSession()

    def __enter__(self) -> DatabaseHandler:
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

    def read_all[U](self, resource_type: type[U], filter: Optional[Condition] = None) -> list[U]:
        db_type = RETURN_TO_DB_TYPE_MAP[resource_type]
        query = self.session.query(db_type)

        if filter is not None:
            sql_condition = condition_to_sqlalchemy(resource_type, filter)
            query = query.filter(sql_condition)

        db_resources = query.all()
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
    

def condition_to_sqlalchemy(resource_type: type[Any], condition: Condition) -> Any:
    if isinstance(condition, FilterCondition):
        return filter_condition_to_sqlalchemy(resource_type, condition)
    elif isinstance(condition, JointCondition):
        return joint_condition_to_sqlalchemy(resource_type, condition)


def filter_condition_to_sqlalchemy(resource_type: type[Any], condition: FilterCondition):
    attribute = getattr(RETURN_TO_DB_TYPE_MAP[resource_type], condition.attribute)
    return CONDITION_TO_SQLALCHEMY_OPERATOR_MAP[condition.operator](attribute, condition.value)


def joint_condition_to_sqlalchemy(resource_type: type[Any], condition: JointCondition):
    cond_left = condition_to_sqlalchemy(resource_type, condition.left)
    cond_right = condition_to_sqlalchemy(resource_type, condition.right)

    if condition.operator == ConditionsJoinOperator.AND:
        return and_(cond_left, cond_right)
    elif condition.operator == ConditionsJoinOperator.OR:
        return or_(cond_left, cond_right)