from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM
from core.multi_database_middleware import DeclarativeBase as Base
from models.model_enums import VehicleTypeEnum
from models.booking_model import BookingDatesModel

class UserModel(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True) 
    date_joined =  Column(DateTime(timezone=True), server_default=func.now(), nullable=False) 
    last_login =   Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)    
    first_name =   Column(String, unique=False, index=False, nullable=False)
    last_name =    Column(String, unique=False, index=False, nullable=False)
    email =        Column(String, unique=True, index=False, nullable=False)
    password =     Column(String, unique=False, index=False, nullable=False)
    vehicle_type = Column(
        ENUM(VehicleTypeEnum, name='user_vehicle_type', values_callable=lambda obj: [e.value for e in obj]),
        nullable=False,
        default=VehicleTypeEnum.CAR.value,
        server_default=VehicleTypeEnum.CAR.value
    )
    license_plate = Column(String, unique=False, index=False, nullable=False)

    booking = relationship("BookingDatesModel", back_populates="user")
