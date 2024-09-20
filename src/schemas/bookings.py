from datetime import date

from pydantic import BaseModel


class BookingRequestAdd(BaseModel):
    date_from: date
    date_to: date
    room_id: int


class BookingAdd(BookingRequestAdd):
    user_id: int
    price: int


class Booking(BookingAdd):
    id: int
