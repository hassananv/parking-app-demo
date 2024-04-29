from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from api.schemas.booking_schema import BookingBase
from models.model_enums import VehicleTypeEnum
#___________________________
class SpotBase(BaseModel):    
     
    name: str
    type: VehicleTypeEnum    
    disabled: Optional[bool]

    booking: Optional[List[BookingBase]] = None
    

    class Config():
        from_attributes = True
        populate_by_name = True
#___________________________


class SpotSchema(SpotBase):
    id: int
    available: Optional[bool]



class SpotSearchSchema(BaseModel):
    start_date: datetime
    end_date: datetime 
    
