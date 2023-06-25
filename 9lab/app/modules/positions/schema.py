from pydantic import BaseModel


class PositionRead(BaseModel):
    id: int
    position_name: str
