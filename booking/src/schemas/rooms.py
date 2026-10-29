from pydantic import BaseModel, Field

from src.schemas.conveniences import ConvenienceSchema


class RoomAddRequestSchema(BaseModel):
    title: str
    description: str | None = Field(None)
    price: int
    quantity: int
    convenience_ids: list[int] = []


class RoomAddSchema(BaseModel):
    title: str
    description: str | None = Field(None)
    hotel_id: int
    price: int
    quantity: int


class RoomSchema(RoomAddSchema):
    id: int


class RoomSchemaWithConveniences(RoomSchema):
    conveniences: list[ConvenienceSchema]


class RoomPatchRequestSchema(BaseModel):
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    convenience_ids: list[int] = []


class RoomPatchSchema(BaseModel):
    title: str | None = Field(None)
    description: str | None = Field(None)
    hotel_id: int | None = Field(None)
    price: int | None = Field(None)
