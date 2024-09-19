from pydantic import BaseModel, Field


class RoomRequestAdd(BaseModel):
    title: str
    description: str | None = Field(None)
    price: int
    quantity: int


class RoomAdd(RoomRequestAdd):
    hotel_id: int


class Room(RoomAdd):
    id: int


class RoomPATCH(BaseModel):
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)
