from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status
from app.core.db import get_session
from app.models import Job
from app.modules.job.schema import JobRead, JobNewEmployee, JobDismissal

router = APIRouter(prefix='/job')


@router.post('/job_new_employee', response_model=JobRead, status_code=status.HTTP_200_OK)
def job_new_emp(
        data: JobNewEmployee,
        db: Session = Depends(get_session)):
    new_emp = Job(**data.dict())

    try:
        db.add(new_emp)
        db.commit()
        db.refresh(new_emp)
    except IntegrityError:
        db.rollback()
        return JobRead(
            error='No employee',
            **new_emp.to_dict())

    return JobRead(
        employee=new_emp.employee.to_dict(),
        **new_emp.to_dict())


@router.put('/job_dismissal', response_model=JobRead, status_code=status.HTTP_200_OK)
def job_dismissal(
        id: int,
        data: JobDismissal,
        db: Session = Depends(get_session)):

    dismissal_emp = db.get(Job, id)

    values = data.dict()
    dismissal_emp.update(**values)

    try:
        db.add(dismissal_emp)
        db.commit()
    except IntegrityError:
        db.rollback()

    return dismissal_emp.to_dict()
