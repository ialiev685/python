from pydantic import BaseModel


class RoomAddSchema(BaseModel):
    title: str
    description: str
    hotel_id: int
    price: int


class RoomSchema(RoomAddSchema):
    id: int
    quantity: int
