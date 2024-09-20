from fastapi import APIRouter, Body, HTTPException

from repositories.hotels import HotelsRepository
from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomAdd, RoomPATCH, RoomRequestAdd

router = APIRouter(prefix='/hotels', tags=['Номера'])


@router.get('/{hotel_id}/rooms')
async def get_rooms(hotel_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_filtered(hotel_id=hotel_id)


@router.get('/{hotel_id}/rooms/{room_id}')
async def get_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        return await (
            RoomsRepository(session)
            .get_one_or_none(hotel_id=hotel_id, id=room_id)
        )


@router.post('/{hotel_id}/rooms')
async def create_room(hotel_id: int, room_data: RoomRequestAdd = Body(openapi_examples={
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
    new_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).get_one_or_none(id=hotel_id)
        if not hotel:
            raise HTTPException(
                status_code=400,
                detail='Отель не существует'
            )
        room = await RoomsRepository(session).add(new_data)
        await session.commit()

    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(hotel_id: int, room_id: int, room_data: RoomRequestAdd):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(
            room_data, id=room_id, hotel_id=hotel_id
        )
        await session.commit()

    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def partially_edit_room(
    hotel_id: int, room_id: int, room_data: RoomPATCH
):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(
            room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id
        )
        await session.commit()

    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id, hotel_id=hotel_id)
        await session.commit()

    return {"status": "OK"}
