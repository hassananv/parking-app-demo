from faulthandler import disable
from sqlalchemy import Column, Integer, String, DateTime, func, Float, Boolean
from core.multi_database_middleware import DeclarativeBase as Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM
from models.model_enums import VehicleTypeEnum


class SpotModel(Base):
    __tablename__ = "spot"

    id = Column(Integer, primary_key=True, index=True)
    created_at =   Column(DateTime(timezone=True), server_default=func.now(), nullable=False)      
    
  
    name = Column(String, unique=False, index=False, nullable=True)
    type = Column(
        ENUM(VehicleTypeEnum, name='user_vehicle_type', values_callable=lambda obj: [e.value for e in obj]),
        nullable=False,
        default=VehicleTypeEnum.CAR.value,
        server_default=VehicleTypeEnum.CAR.value
    )
    
    disabled = Column(Boolean, nullable=False, default=False)

    booking = relationship ("BookingDatesModel", back_populates="spot")
       