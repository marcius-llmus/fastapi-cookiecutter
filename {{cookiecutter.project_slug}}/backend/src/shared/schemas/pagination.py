from src.core.schemas import BaseModel


class Page[TItem](BaseModel):
    items: list[TItem]
    total: int
    limit: int
    offset: int
