from __future__ import annotations
from enum import Enum
from dataclasses import dataclass
from typing import Any, List, Optional, Protocol
from business.exceptions import ResourceNotFoundException


class Operator(Enum):
    EQUALS = "=="
    NOT_EQUALS = "!="
    LESS_THAN = "<"
    LESS_THAN_OR_EQUAL = "<="
    GREATER_THAN = ">"
    GREATER_THAN_OR_EQUAL = ">="


class ConditionsJoinOperator(Enum):
    AND = "AND"
    OR = "OR"


class Condition:
    pass


@dataclass
class FilterCondition(Condition):
    attribute: str
    operator: Operator
    value: Any


@dataclass
class JointCondition(Condition):
    left: Condition
    operator: ConditionsJoinOperator
    right: Condition


class DataStorageInterface(Protocol):
    def __enter__(self) -> DataStorageInterface:
        ...
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        ...

    def commit(self) -> None:
        ...

    def create[T, U](self, resource: T) -> U:
        ...

    def read[U](self, resource_type: type[U], resource_id: int) -> U | None:
        ...

    def read_all[U](self, resource_type: type[U], filter: Optional[Condition] = None) -> list[U]:
        ...

    def update[U](self, resource: U) -> U | None:
        ...

    def delete[U](self, resource_type: type[U], resource_id: int) -> U | None:
        ...


def get_resource[U](dsi: DataStorageInterface, resource_type: type[U], resource_id: int) -> U:
    resource = dsi.read(resource_type, resource_id)
    if resource is None:
        raise ResourceNotFoundException(f"{resource_type.name()} {resource_id} not found.")
    return resource


def get_all_resources[U](dsi: DataStorageInterface, resource_type: type[U]) -> list[U]:
    return dsi.read_all(resource_type)


def create_resource[T, U](dsi: DataStorageInterface, resource: T) -> U:
    created_resource = dsi.create(resource)
    return created_resource
    

def update_resource[U](dsi: DataStorageInterface, resource: U) -> U:
    updated_resource = dsi.update(resource)
    if updated_resource is None:
        raise ResourceNotFoundException(f"{resource.name()} {resource.id} not found.")
    return updated_resource


def delete_resource[U](dsi: DataStorageInterface, resource_type: type[U], resource_id: int) -> U:
    deleted_resource = dsi.delete(resource_type, resource_id)
    if deleted_resource is None:
        raise ResourceNotFoundException(f"{resource_type.name()} {resource_id} not found.")
    return deleted_resource