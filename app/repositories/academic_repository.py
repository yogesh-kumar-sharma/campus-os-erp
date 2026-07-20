"""Database operations for normalized academic entities."""

from typing import Generic, TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class AcademicRepository(Generic[ModelType]):
    """Small reusable repository for catalog entities."""

    def __init__(self, session: AsyncSession, model: type[ModelType]) -> None:
        self.session = session
        self.model = model

    async def get(self, entity_id: UUID) -> ModelType | None:
        return await self.session.get(self.model, entity_id)

    async def list(self) -> list[ModelType]:
        result = await self.session.execute(select(self.model).order_by(self.model.created_at.desc()))
        return list(result.scalars())

    async def create(self, **values: object) -> ModelType:
        entity = self.model(**values)
        self.session.add(entity)
        await self.session.flush()
        return entity
