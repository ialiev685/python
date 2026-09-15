from src.schemas.conveniences import ConvenienceSchema
from src.repositories.base import BaseRepository
from src.models.conveniences import ConveniencesModel


class ConveniencesRepository(BaseRepository):
    model = ConveniencesModel
    schema = ConvenienceSchema
