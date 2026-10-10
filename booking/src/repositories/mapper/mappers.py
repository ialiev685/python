from src.models.conveniences import ConveniencesModel, RoomConveniencesModel
from src.models.rooms import RoomsModel
from src.models.users import UsersModel
from src.schemas.conveniences import ConvenienceSchema, RoomConvenienceSchema
from src.models.hotels import HotelsModel
from src.schemas.hotels import HotelSchema
from src.repositories.mapper.base import DataMapper
from src.models.bookings import BookingsModel
from src.schemas.bookings import BookingSchema
from src.schemas.rooms import RoomSchema, RoomSchemaWithConveniences
from src.schemas.users import UserSchema, UserWithHashedPasswordSchema


class BookingDataMapper(DataMapper):
    db_model = BookingsModel
    schema = BookingSchema


class HotelsDataMapper(DataMapper):
    db_model = HotelsModel
    schema = HotelSchema


class ConveniencesDataMapper(DataMapper):
    db_model = ConveniencesModel
    schema = ConvenienceSchema


class RoomConveniencesDataMapper(DataMapper):
    db_model = RoomConveniencesModel
    schema = RoomConvenienceSchema


class RoomDataMapper(DataMapper):
    db_model = RoomsModel
    schema = RoomSchema


class RoomWithConveniencesDataMapper(DataMapper):
    db_model = RoomsModel
    schema = RoomSchemaWithConveniences


class UsersDataMapper(DataMapper):
    db_model = UsersModel
    schema = UserSchema


class UserWithHashedPasswordDataMapper(DataMapper):
    db_model = UsersModel
    schema = UserWithHashedPasswordSchema
