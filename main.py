import uvicorn
from fastapi import FastAPI, Query, Body

app = FastAPI()

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
]


@app.get("/hotels")
def get_hotels(
    id: int | None = Query(None, description="Айдишник"),
    title: str | None = Query(None, description="Название отеля"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_


@app.post("/hotels")
def create_hotel(
    title: str = Body(embed=True),
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title
    })
    return {"status": "OK"}


@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@app.put("/hotels/{hotel_id}")
def put_hotel(hotel_id: int, title: str = Body(), name: str = Body()):
    global hotels
    for hotel in hotels:
        if hotel['id'] != hotel_id:
            continue
        hotel['title'] = title
        hotel['name'] = name
    return {'status': 'OK'}


@app.patch("/hotels/{hotel_id}")
def patch_hotel(
    hotel_id: int,
    title: str | None = Body(None), name: str | None = Body(None)
):
    global hotels
    for hotel in hotels:
        if hotel['id'] != hotel_id:
            continue
        if title:
            hotel['title'] = title
        if name:
            hotel['name'] = name
    return {'status': 'OK'}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
