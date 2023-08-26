from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Boolean
from core.multi_database_middleware import DeclarativeBase as Base
from sqlalchemy.orm import relationship
from models.spot_model import SpotModel



class BookingDatesModel(Base):
    __tablename__ = 'booking_dates'

    id =         Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)    
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date =   Column(DateTime(timezone=True), nullable=False)    
    timezone =   Column(String, unique=False, index=False, nullable=False)
    license_plate = Column(String, unique=False, index=False, nullable=True)

    spot_id = Column(Integer, ForeignKey('spot.id', ondelete="CASCADE"))
    spot = relationship("SpotModel", back_populates="booking")

    user_id = Column(Integer, ForeignKey('user.id', ondelete="CASCADE"))
    user = relationship("UserModel", back_populates="booking")
