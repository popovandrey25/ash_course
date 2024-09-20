from fastapi import APIRouter, Body

from src.api.dependencies import DBDep
from src.schemas.rooms import RoomAdd, RoomPATCH, RoomRequestAdd

router = APIRouter(prefix='/hotels', tags=['Номера'])


@router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int, db: DBDep):
    return await db.rooms.get_filtered(hotel_id=hotel_id)


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post('/{hotel_id}/rooms')
async def create_room(
    hotel_id: int, db: DBDep,
    room_data: RoomRequestAdd = Body(openapi_examples={
        "1": {
            "summary": "Президентский люкс",
            "value": {
                "title": "Президентский люкс",
                "description": "Комфортабельный номер",
                "price": 200,
                "quantity": 2
            }
        },
        "2": {
            "summary": "Одноместный эконом",
            "value": {
                "title": "Одноместный эконом",
                "description": "Недорогой номер",
                "price": 15,
                "quantity": 10
            }
        }
    })
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)
    await db.commit()

    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(
    hotel_id: int, room_id: int, room_data: RoomRequestAdd, db: DBDep
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(_room_data, id=room_id)
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def partially_edit_room(
    hotel_id: int, room_id: int, room_data: RoomPATCH, db: DBDep
):
    await db.rooms.edit(
        room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id
    )
    await db.commit()


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}
