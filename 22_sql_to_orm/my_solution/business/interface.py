from __future__ import annotations
from typing import Protocol
from business.exceptions import ResourceNotFoundException


class DataStorageInterface(Protocol):
    def __enter__(self) -> DataStorageInterface:
        ...
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        ...

    def commit(self) -> None:
        ...

    def read[U](self, resource_type: type[U], resource_id: int) -> U | None:
        ...

    def read_all[U](self, resource_type: type[U]) -> list[U]:
        ...

    def create[T, U](self, resource: T) -> U:
        ...

    def update[U](self, resource: U) -> U | None:
        ...

    def delete[U](self, resource_type: type[U], resource_id: int) -> U | None:
        ...


def get_resource[U](dsi: DataStorageInterface, resource_type: type[U], resource_id: int) -> U:
    with dsi:
        resource = dsi.read(resource_type, resource_id)
        if resource is None:
            raise ResourceNotFoundException(f"{resource_type.name()} {resource_id} not found.")
        return resource


def get_all_resources[U](dsi: DataStorageInterface, resource_type: type[U]) -> list[U]:
    with dsi:
        return dsi.read_all(resource_type)


def create_resource[T, U](dsi: DataStorageInterface, resource: T) -> U:
    with dsi:
        created_resource = dsi.create(resource)
        dsi.commit()
        return created_resource
    

def update_resource[U](dsi: DataStorageInterface, resource: U) -> U:
    with dsi:
        updated_resource = dsi.update(resource)
        if updated_resource is None:
            raise ResourceNotFoundException(f"{resource.name()} {resource.id} not found.")
        dsi.commit()
        return updated_resource


def delete_resource[U](dsi: DataStorageInterface, resource_type: type[U], resource_id: int) -> U:
    with dsi:
        deleted_resource = dsi.delete(resource_type, resource_id)
        if deleted_resource is None:
            raise ResourceNotFoundException(f"{resource_type.name()} {resource_id} not found.")
        dsi.commit()
        return deleted_resource