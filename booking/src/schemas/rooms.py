from pydantic import BaseModel, Field


class RoomAddRequestSchema(BaseModel):
    title: str
    description: str
    price: int
    quantity: int


class RoomAddSchema(BaseModel):
    title: str
    description: str
    hotel_id: int
    price: int
    quantity: int


class RoomSchema(RoomAddSchema):
    id: int


class RoomPatchRequestSchema(BaseModel):
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)


class RoomPatchSchema(BaseModel):
    title: str | None = Field(None)
    description: str | None = Field(None)
    hotel_id: int | None = Field(None)
    price: int | None = Field(None)
