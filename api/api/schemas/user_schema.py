from typing import Optional
from pydantic import BaseModel
from models.model_enums import VehicleTypeEnum 

#___________________________
class UserBase(BaseModel):

    first_name: str
    last_name: str
    email: str    
    vehicle_type: VehicleTypeEnum    
    license_plate: str
 

    class Config():
        orm_mode = True
        allow_population_by_field_name = True
#___________________________


class UserSchema(UserBase):
    id: int       


class UserRegisterSchema(UserBase):
    password: str 


class UserUpdateSchema(UserBase):
    id:int
    password: Optional[str]
    old_password: Optional[str]
    



class UserLogInSchema(BaseModel):
    email: str    
    password: str
