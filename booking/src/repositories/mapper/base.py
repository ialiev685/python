from typing import TypeVar
from pydantic import BaseModel
from src.database import Base

Schema = TypeVar('Schema', bound=BaseModel)
Model = TypeVar('Model', bound=Base)


class DataMapper:
    db_model: Model = None
    schema: Schema = None

    @classmethod
    def from_orm(cls, data):
        return cls.schema.model_validate(data, from_attributes=True)

    @classmethod
    def to_orm(cls, data: BaseModel):
        return cls.db_model(**data.model_dump())
