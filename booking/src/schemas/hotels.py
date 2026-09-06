from pydantic import BaseModel, Field


class HotelAddSchema(BaseModel):
    title: str
    location: str


class HotelSchema(HotelAddSchema):
    id: int


class HotelPatchSchema(BaseModel):
    title: str | None = Field(None)
    location: str | None = Field(None)
