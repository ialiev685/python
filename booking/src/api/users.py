from fastapi import APIRouter, status, HTTPException, Response, Request
from schemas.users import UserRequestAddSchema, UserAddSchema
from src.services.auth import AuthService
from src.database import async_session_marker
from src.repositories.users import UsersRepository

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(data: UserRequestAddSchema):
    hashed_password = AuthService().password_hash.hash(data.password)
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
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Неверный логин или пароль.')
        token = AuthService().create_access_token(data={'user_id': user.id})
        response.set_cookie(key='access_token', value=token)
        return {"status": status.HTTP_200_OK, 'access_token': token}


@router.get('/only_auth')
async def only_auth(request: Request):
    access_token = request.cookies.get('access_token', None)
    print('access_token', access_token)
