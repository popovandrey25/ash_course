from sqlalchemy import delete, select, insert, update
from pydantic import BaseModel


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def add(self, model_data: BaseModel):
        add_object_stmt = (
            insert(self.model)
            .values(**model_data.model_dump())
            .returning(self.model)
        )
        result = await self.session.execute(add_object_stmt)
        return result.scalars().one()

    async def edit(self, model_data: BaseModel, **filter_by):
        update_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**model_data.model_dump())
        )
        await self.session.execute(update_stmt)

    async def delete(self, **filter_by):
        delete_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_stmt)
