from typing import Optional
from pydantic import BaseModel
from models.model_enums import VehicleTypeEnum 

#___________________________
class UserBase(BaseModel):

    first_name: str
    last_name: str
    email: str    
    vehicle_type: VehicleTypeEnum    
    license_plate: Optional[str]
 

    class Config():
        from_attributes = True
        populate_by_name = True
#___________________________


class UserSchema(UserBase):
    id: int       


class UserRegisterSchema(UserBase):
    password: str 


class UserUpdateSchema(UserBase):
    id:int
    password: Optional[str] = None
    old_password: Optional[str] = None

    class Config():
        from_attributes = True
        populate_by_name = True
    



class UserLogInSchema(BaseModel):
    email: str    
    password: str
