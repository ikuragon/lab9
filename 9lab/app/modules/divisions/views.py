from fastapi import APIRouter, Depends
# from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status
from app.core.db import get_session
from app.models import Division
from app.modules.divisions.schema import DivisionRead

router = APIRouter(prefix='/division')


@router.post('/create', status_code=status.HTTP_200_OK)
def add_division(
        division_name: str,
        db: Session = Depends(get_session)):
    new_division = Division(division_name=division_name)

    try:
        db.add(new_division)
        db.commit()
    except IntegrityError:
        db.rollback()
        return status.HTTP_500_INTERNAL_SERVER_ERROR

    return new_division.to_dict()


@router.put('/delete', response_model=DivisionRead, status_code=status.HTTP_200_OK)
def delete_division(
        id: int,
        db: Session = Depends(get_session)):
    del_division = db.get(Division, id)

    try:
        db.delete(del_division)
        db.commit()
    except IntegrityError:
        db.rollback()
    return 'division deleted'


@router.get('/{id}', status_code=status.HTTP_200_OK)
def get_division(
        id: int,
        db: Session = Depends(get_session)):
    division = db.get(Division, id)

    if not division:
        return status.HTTP_404_NOT_FOUND

    return division.to_dict()
