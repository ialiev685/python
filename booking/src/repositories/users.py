from sqlalchemy import select
from pydantic import EmailStr
from src.repositories.base import BaseRepository
from src.models.users import UsersModel
from src.schemas.users import User, UserWithHashedPasswordSchema


class UsersRepository(BaseRepository):
    model = UsersModel
    schema = User

    async def get_one_or_none_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one()
        return UserWithHashedPasswordSchema.model_validate(model, from_attributes=True)
