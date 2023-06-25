from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status
from app.core.db import get_session
from app.models import Employee
from app.modules.employees.schema import EmployeeRead, EmployeeUpdate

router = APIRouter(prefix='/employee')


@router.post('/create', status_code=status.HTTP_200_OK)
def add_employee(
        second_name: str,
        first_name: str,
        surname: str,
        address: str,
        date_of_birth: str,
        db: Session = Depends(get_session)
):
    new_emp = Employee(second_name=second_name, first_name=first_name,
                       surname=surname, address=address,
                       date_of_birth=date_of_birth)

    try:
        db.add(new_emp)
        db.commit()
    except IntegrityError:
        db.rollback()
        return "status.HTTP_500_INTERNAL_SERVER_ERROR"

    return new_emp.to_dict()


@router.put('/update', response_model=EmployeeRead, status_code=status.HTTP_200_OK)
def update_employee(
        id: int,
        data: EmployeeUpdate,
        db: Session = Depends(get_session)):
    update_emp = db.get(Employee, id)

    values = data.dict()
    update_emp.update(**values)

    try:
        db.add(update_emp)
        db.commit()
    except IntegrityError:
        db.rollback()

    return update_emp.to_dict()


@router.get('/all', status_code=status.HTTP_200_OK)
def get_all_employees(
        first_name: str = None,
        db: Session = Depends(get_session)):
    query = select(Employee)

    if first_name:
        query = query.where(Employee.first_name == first_name)

    all_emp = db.scalars(query).all()

    return [employee.to_dict() for employee in all_emp]


@router.get('/{id}', status_code=status.HTTP_200_OK)
def get_employee(
        id: int,
        db: Session = Depends(get_session)):
    get_emp = db.get(Employee, id)

    if not get_emp:
        return status.HTTP_404_NOT_FOUND
    return get_emp.to_dict()


@router.put('/delete', response_model=EmployeeRead, status_code=status.HTTP_200_OK)
def delete_employee(
        id: int,
        db: Session = Depends(get_session)
):
    del_emp = db.get(Employee, id)

    try:
        db.delete(del_emp)
        db.commit()
    except IntegrityError:
        db.rollback()
    return 'employee deleted'
