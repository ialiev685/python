from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import delete, select

from src.schemas.conveniences import ConvenienceSchema, RoomConvenienceSchema
from src.repositories.base import BaseRepository
from src.models.conveniences import ConveniencesModel, RoomConveniencesModel


class ConveniencesRepository(BaseRepository):
    model = ConveniencesModel
    schema = ConvenienceSchema


class RoomConveniencesRepository(BaseRepository):
    model = RoomConveniencesModel
    schema = RoomConvenienceSchema

    async def set_room_conveniences(self, room_id: int, convenience_ids: list[int]):
        query = select(self.model.convenience_id).filter_by(room_id=room_id)
        response = await  self.session.execute(query)
        current_convenience_ids: list[int] = response.scalars().all()

        delete_convenience_ids: list[int] = list(set(current_convenience_ids) - set(convenience_ids))
        insert_convenience_ids: list[int] = list(set(convenience_ids) - set(current_convenience_ids))

        if delete_convenience_ids:
            delete_stmt = delete(self.model).filter(
                self.model.room_id == room_id,
                self.model.convenience_id.in_(delete_convenience_ids))
            await self.session.execute(delete_stmt)

        if insert_convenience_ids:
            insert_stmt = insert(self.model).values(
                [{'room_id': room_id, 'convenience_id': _id} for _id in insert_convenience_ids])
            await self.session.execute(insert_stmt)
