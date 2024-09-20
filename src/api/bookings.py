from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAdd, BookingRequestAdd

router = APIRouter(prefix='/bookings', tags=['Бронирования'])


@router.post('')
async def add_booking(
    booking_data: BookingRequestAdd, user_id: UserIdDep, db: DBDep
):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    if not room:
        raise HTTPException(status_code=400, detail='Номер для бронирования не найден')
    _booking_data = BookingAdd(
        user_id=user_id, price=room.price, **booking_data.model_dump()
    )
    booking = await db.bookings.add(_booking_data)
    return {'status': 'OK', 'booking': booking}
