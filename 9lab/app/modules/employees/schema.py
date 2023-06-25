from pydantic import BaseModel


class EmployeeRead(BaseModel):
    id: int
    second_name: str
    first_name: str
    surname: str
    address: str
    date_of_birth: str


class EmployeeUpdate(BaseModel):
    second_name: str
    first_name: str
    surname: str
    address: str
    date_of_birth: str
