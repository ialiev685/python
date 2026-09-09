from sqlalchemy import select
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsModel
from src.schemas.rooms import RoomSchema


class RoomRepository(BaseRepository):
    model = RoomsModel
    schema = RoomSchema

    # async def get_all(
    #         self,
    #         title,
    #         description,
    #         hotel_id
    # ):
    #     query = select(RoomsModel).where(RoomsModel.hotel_id == hotel_id)
    #     if title:
    #         query = query.where(RoomsModel.title.icontains(title))
    #     if description:
    #         query = query.where(RoomsModel.description.icontains(description))
    #
    #     self.debug(request=query)
    #     result = await self.session.execute(query)
    #     return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]
