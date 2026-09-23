from pydantic import BaseModel


class ConvenienceAddRequestSchema(BaseModel):
    title: str


class ConvenienceSchema(ConvenienceAddRequestSchema):
    id: int


class RoomConvenienceAddRequestSchema(BaseModel):
    room_id: int
    convenience_id: int


class RoomConvenienceSchema(BaseModel):
    id: int
