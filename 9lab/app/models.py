from sqlalchemy import inspect, Integer, Column, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core.db import Base


class BaseMixin(Base):
    __abstract__ = True

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def update(self, **kwargs) -> None:
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in
                inspect(self).mapper.column_attrs}


class Employee(BaseMixin):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True)
    second_name = Column(String(30), nullable=False)
    first_name = Column(String(30), nullable=False)
    surname = Column(String(30), nullable=False)
    address = Column(String(100), nullable=False)
    date_of_birth = Column(String, nullable=False)


class Position(BaseMixin):
    __tablename__ = 'positions'

    id = Column(Integer, primary_key=True)
    position_name = Column(String(50), nullable=False)


class Division(BaseMixin):
    __tablename__ = 'divisions'

    id = Column(Integer, primary_key=True)
    division_name = Column(String, nullable=False)


class Job(BaseMixin):
    __tablename__ = 'job'

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    employee = relationship('Employee')
    position_id = Column(Integer, ForeignKey('positions.id'))
    position = relationship('Position')
    division_id = Column(Integer, ForeignKey('divisions.id'))
    division = relationship('Division')
    date_of_employment = Column(String, nullable=True)
    date_of_dismissal = Column(String, nullable=True)
