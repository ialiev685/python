from sqlalchemy import select
from pydantic import EmailStr
from sqlalchemy.exc import NoResultFound

from src.exceptions import NotFoundException
from src.repositories.base import BaseRepository
from src.models.users import UsersModel

from src.repositories.mapper.mappers import UsersDataMapper, UserWithHashedPasswordDataMapper


class UsersRepository(BaseRepository):
    model = UsersModel
    mapper = UsersDataMapper

    async def get_one_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        self.debug(request=query)
        result = await self.session.execute(query)
        try:
            model = result.scalar_one()
        except NoResultFound:
            raise NotFoundException

        return UserWithHashedPasswordDataMapper.from_orm(model)
