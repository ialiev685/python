from pydantic import BaseModel


class ConvenienceAddRequestSchema(BaseModel):
    title: str


class ConvenienceSchema(ConvenienceAddRequestSchema):
    id: int
