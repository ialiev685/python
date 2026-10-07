from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base


class ConveniencesModel(Base):
    __tablename__ = "conveniences"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(length=100))

    rooms: Mapped[list['RoomsModel']] = relationship(secondary='room_conveniences', back_populates='conveniences')


class RoomConveniencesModel(Base):
    __tablename__ = "room_conveniences"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey('rooms.id'))
    convenience_id: Mapped[int] = mapped_column(ForeignKey('conveniences.id'))

    __table_args__ = (
        UniqueConstraint('convenience_id', 'room_id'),
    )
