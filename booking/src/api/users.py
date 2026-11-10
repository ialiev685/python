from fastapi import APIRouter, status, HTTPException, Response
from src.schemas.users import UserRequestAddSchema, UserAddSchema
from src.services.auth import AuthService
from src.api.dependencies import UserIdDep, DBDep

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(data: UserRequestAddSchema, db: DBDep):
    hashed_password = AuthService().password_hash.hash(data.password)
    await  db.users.add(
        data=UserAddSchema(email=data.email, hashed_password=hashed_password)
    )
    await db.commit()

    return {"status": status.HTTP_200_OK}


@router.post('/login')
async def login_user(data: UserRequestAddSchema, response: Response, db: DBDep):
    user = await db.users.get_one_or_none_with_hashed_password(email=data.email)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Пользователь с {data.email} не существует.")
    if not AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Неверный логин или пароль.')
    token = AuthService().create_access_token(data={'user_id': user.id})
    response.set_cookie(key='access_token', value=token)
    return {"status": status.HTTP_200_OK, 'access_token': token}


@router.get('/me')
async def get_me(user_id: UserIdDep, db: DBDep):
    user = await db.users.get_one_or_none(id=user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Не авторизирован')
    return user


@router.post('/logout')
async def logout_user(response: Response, db: DBDep):
    response.delete_cookie('access_token')
    return {"status": status.HTTP_200_OK}
