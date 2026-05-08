from uuid import UUID

from src.core.schemas import BaseModel


class IdResponse(BaseModel):
    id: UUID
