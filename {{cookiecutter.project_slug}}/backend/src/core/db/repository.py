from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db.base import Base
from src.core.schemas import BaseModel


class BaseRepository[T: Base]:
    model: type[T]

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get(self, pk: object) -> T | None:
        return await self.db.get(self.model, pk)

    async def create(self, obj_in: BaseModel) -> T:
        db_obj = self.model(**obj_in.model_dump())
        self.db.add(db_obj)
        await self.db.flush()
        return db_obj

    async def update(self, *, db_obj: T, obj_in: BaseModel) -> T:
        update_data = obj_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_obj, key, value)
        await self.db.flush()
        await self.db.refresh(db_obj)
        return db_obj

    async def delete(self, *, pk: object) -> T | None:
        db_obj = await self.db.get(self.model, pk)
        if db_obj is None:
            return None
        await self.db.delete(db_obj)
        await self.db.flush()
        return db_obj
