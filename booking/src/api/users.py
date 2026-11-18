from fastapi import APIRouter, status, Response

from src.exceptions import (
    UserAlreadyExistsHTTPException,
    UserAlreadyExistsException,
    UserNotFoundException,
    UserNotFoundHTTPException,
    IncorrectUserOrPasswordException,
    IncorrectUserOrPasswordHTTPException
)
from src.schemas.users import UserRequestAddSchema, UserAddSchema
from src.services.auth import AuthService
from src.api.dependencies import UserIdDep, DBDep

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(data: UserRequestAddSchema, db: DBDep):
    try:
        await AuthService(db=db).register_user(data=data)
        return {"status": status.HTTP_200_OK}
    except UserAlreadyExistsException:
        raise UserAlreadyExistsHTTPException


@router.post('/login')
async def login_user(data: UserRequestAddSchema, response: Response, db: DBDep):
    try:
        token = await AuthService(db=db).login_user(data=data)
        response.set_cookie(key='access_token', value=token)
        return {"status": status.HTTP_200_OK, 'access_token': token}
    except UserNotFoundException:
        raise UserNotFoundHTTPException
    except IncorrectUserOrPasswordException:
        raise IncorrectUserOrPasswordHTTPException


@router.get('/me')
async def get_me(user_id: UserIdDep, db: DBDep):
    try:
        user = await AuthService(db=db).get_me(user_id=user_id)
        return user
    except UserNotFoundException:
        raise UserNotFoundHTTPException


@router.post('/logout')
async def logout_user(response: Response, db: DBDep):
    response.delete_cookie('access_token')
    return {"status": status.HTTP_200_OK}
