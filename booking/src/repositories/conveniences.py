from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import delete
from fastapi import HTTPException
from pydantic import BaseModel

from src.schemas.conveniences import ConvenienceSchema, RoomConvenienceSchema
from src.repositories.base import BaseRepository
from src.models.conveniences import ConveniencesModel, RoomConveniencesModel


class ConveniencesRepository(BaseRepository):
    model = ConveniencesModel
    schema = ConvenienceSchema


class RoomConveniencesRepository(BaseRepository):
    model = RoomConveniencesModel
    schema = RoomConvenienceSchema

    async def edit_bulk(self, data: list[BaseModel], exclude_unset: bool = False, **filter_by):
        try:
            update_hotel_stmt = (
                insert(RoomConveniencesModel)
                .values([item.model_dump(exclude_unset=exclude_unset) for item in data])
                .on_conflict_do_nothing(
                    index_elements=[RoomConveniencesModel.room_id, RoomConveniencesModel.convenience_id]
                )
                .returning(RoomConveniencesModel)
            )
            self.debug(request=update_hotel_stmt)
            conveniences_ids = await self.session.execute(update_hotel_stmt)

            ids = [RoomConvenienceSchema.model_validate(model, from_attributes=True) for model in
                   conveniences_ids.scalars().all()]
            return ids
        except IntegrityError:
            raise HTTPException(status_code=400, detail="Заданые удобства не существуют")

    async def delete_bulk(self, room_id: int, convenience_ids: list[int]) -> None:
        delete_hotel_stmt = delete(RoomConveniencesModel).filter(
            RoomConveniencesModel.room_id == room_id,
            RoomConveniencesModel.convenience_id.notin_(convenience_ids)
        )
        self.debug(request=delete_hotel_stmt)
        await self.session.execute(delete_hotel_stmt)
