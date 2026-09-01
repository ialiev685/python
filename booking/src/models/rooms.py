from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base


class RoomsModel(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(length=30))
    description: Mapped[str | None]
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    price: Mapped[int]
    quantity: Mapped[int] = mapped_column(Integer, default=1)
