from datetime import timedelta, datetime, timezone

import jwt
from fastapi import APIRouter, HTTPException
from pwdlib import PasswordHash
from src.config import settings
from src.exceptions import IncorrectTokenException, ObjectAlreadyExistsException, UserAlreadyExistsException, \
    UserNotFoundException, ObjectNotFoundException, IncorrectUserOrPasswordException
from src.schemas.users import UserRequestAddSchema, UserAddSchema
from src.services.base import BaseService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


class AuthService(BaseService):
    password_hash = PasswordHash.recommended()

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode |= ({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt

    def verify_password(self, password: str, hashed_password: str):
        return self.password_hash.verify(password, hashed_password)

    def decode_token(self, token: str):
        try:
            return jwt.decode(jwt=token, key=settings.JWT_SECRET_KEY, algorithms=settings.JWT_ALGORITHM)
        except (jwt.exceptions.ExpiredSignatureError, jwt.exceptions.DecodeError):
            raise IncorrectTokenException

    async def register_user(self, data: UserRequestAddSchema):
        hashed_password = self.password_hash.hash(data.password)
        try:
            await  self.db.users.add(data=UserAddSchema(email=data.email, hashed_password=hashed_password))
            await self.db.commit()
        except ObjectAlreadyExistsException as ex:
            raise UserAlreadyExistsException from ex

    async def login_user(self, data: UserRequestAddSchema):
        try:
            user = await self.db.users.get_one_with_hashed_password(email=data.email)
        except ObjectNotFoundException as ex:
            raise UserNotFoundException from ex

        if not self.verify_password(data.password, user.hashed_password):
            raise IncorrectUserOrPasswordException
        token = self.create_access_token(data={'user_id': user.id})
        return token

    async def get_me(self, user_id: int):
        try:
            user = await self.db.users.get_one(id=user_id)
        except ObjectNotFoundException as ex:
            raise UserNotFoundException from ex
        return user
