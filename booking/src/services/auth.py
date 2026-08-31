from datetime import timedelta, datetime, timezone

import jwt
from fastapi import APIRouter
from pwdlib import PasswordHash
from src.config import settings

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


class AuthService:
    password_hash = PasswordHash.recommended()

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode |= ({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt

    def verify_password(self, password: str, hashed_password: str):
        return self.password_hash.verify(password, hashed_password)
