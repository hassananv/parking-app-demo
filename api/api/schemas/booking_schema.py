from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from models.model_enums import VehicleTypeEnum

#___________________________
class BookingBase(BaseModel):    
    
    start_date: datetime
    end_date: datetime    
    timezone: str
    license_plate: Optional[str]
    spot_id: int
    # spot

    class Config():
        orm_mode = True
        allow_population_by_field_name = True
#___________________________

class BookingSchema(BookingBase):
    user_id: int



class SpotShort(BaseModel):
    id: int
    name: str
    type: VehicleTypeEnum
    class Config():
        orm_mode = True

class BookingSpotSchema(BookingBase):
    spot: SpotShort
    id: int