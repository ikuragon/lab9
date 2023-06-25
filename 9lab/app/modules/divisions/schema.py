from pydantic import BaseModel


class DivisionRead(BaseModel):
    id: int
    division_name: str


# class DivisionUpdate(BaseModel):
#     division_name: str
