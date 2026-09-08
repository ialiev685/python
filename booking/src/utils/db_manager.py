from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from src.repositories.hotels import HotelsRepository
from src.repositories.rooms import RoomRepository
from src.repositories.users import UsersRepository


class DBManager:
    session_factory: async_sessionmaker[AsyncSession]

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()
        self.hotels = HotelsRepository(session=self.session)
        self.rooms = RoomRepository(session=self.session)
        self.users = UsersRepository(session=self.session)
        return self

    async def __aexit__(self, *args):
        await  self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()
