from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base


class ConveniencesModel(Base):
    __tablename__ = "conveniences"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(length=100))


class RoomConveniencesModel(Base):
    __tablename__ = "room_conveniences"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey('rooms.id'))
    convenience_id: Mapped[int] = mapped_column(ForeignKey('conveniences.id'))
