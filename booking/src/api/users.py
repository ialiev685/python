from datetime import timedelta, datetime, timezone

import jwt
from fastapi import APIRouter, status, HTTPException, Response
from pwdlib import PasswordHash

from schemas.users import UserRequestAddSchema, UserAddSchema
from src.database import async_session_marker
from src.repositories.users import UsersRepository

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

password_hash = PasswordHash.recommended()

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode |= ({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(password: str, hashed_password: str):
    return password_hash.verify(password, hashed_password)


@router.post("/register")
async def register_user(data: UserRequestAddSchema):
    hashed_password = password_hash.hash(data.password)
    async with async_session_marker() as session:
        await UsersRepository(session=session).add(
            data=UserAddSchema(email=data.email, hashed_password=hashed_password))
        await session.commit()

    return {"status": status.HTTP_200_OK}


@router.post('/login')
async def login_user(data: UserRequestAddSchema, response: Response):
    async with async_session_marker() as session:
        user = await UsersRepository(session=session).get_one_or_none_with_hashed_password(email=data.email)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail=f"Пользователь с {data.email} не существует.")
        if not verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Неверный логин или пароль.')
        token = create_access_token(data={'user_id': user.id})
        response.set_cookie(key='access_token', value=token)
        return {"status": status.HTTP_200_OK, 'access_token': token}
