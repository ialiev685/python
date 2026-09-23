from src.schemas.conveniences import ConvenienceSchema, RoomConvenienceSchema
from src.repositories.base import BaseRepository
from src.models.conveniences import ConveniencesModel, RoomConveniencesModel


class ConveniencesRepository(BaseRepository):
    model = ConveniencesModel
    schema = ConvenienceSchema


class RoomConveniencesRepository(BaseRepository):
    model = RoomConveniencesModel
    schema = RoomConvenienceSchema
