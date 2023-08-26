from fastapi import APIRouter, status, Depends
from core.multi_database_middleware import get_db_session
from sqlalchemy.orm import Session
from api.schemas.user_schema import UserSchema, UserRegisterSchema, UserUpdateSchema
from core.auth import logged_in_user
from api.repository.user_transactions import create_user, modify_user, get_user

router = APIRouter(
    prefix="/user",
    tags=['User']
)




@router.get('/info', status_code=status.HTTP_200_OK , response_model=UserSchema)
def get_Logged_In_User_Info(db: Session= Depends(get_db_session), user = Depends(logged_in_user)):
    return get_user(user['email'], db)




@router.post('/register', status_code=status.HTTP_200_OK)
def register_User(request: UserRegisterSchema, db: Session= Depends(get_db_session)):
    return create_user(request, db)
    



@router.put('/update', status_code=status.HTTP_200_OK)
def update_User_profile(request: UserUpdateSchema, db: Session= Depends(get_db_session), user = Depends(logged_in_user)):
    return modify_user(request, db, user["email"])




