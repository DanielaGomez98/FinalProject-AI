import typing
from sqlalchemy.orm import as_declarative, declared_attr

class_registry: typing.Dict = {}

"""
Base class for sqlalchemy ORM classes.
"""


# this class allows to create a generic class that represents a model (database table).
@as_declarative(class_registry=class_registry)
class OrmBaseModel:
    id: typing.Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
