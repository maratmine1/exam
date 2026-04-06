from sqlalchemy import Boolean, Column, Integer, String

from .database import Base


class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    model = Column(String, nullable=False)
    number = Column(String, nullable=False, unique=True, index=True)
    is_reserved = Column(Boolean, nullable=False, default=False)


class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String, nullable=False, index=True)
    sms_code = Column(String, nullable=False, index=True)
    car_model = Column(String, nullable=False)
    car_number = Column(String, nullable=False, index=True)
    fuel_level = Column(String, nullable=False)

