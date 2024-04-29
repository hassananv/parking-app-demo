from fastapi import APIRouter, status, Depends, Request
from core.multi_database_middleware import get_db_session
from sqlalchemy.orm import Session
from api.schemas.user_schema import UserLogInSchema


from api.repository.auth_transactions import logout_user, authenticate_user, get_access_token

router = APIRouter(
    prefix="/auth",
    tags=['Auth']
)




@router.post('/login', status_code=status.HTTP_200_OK)
def log_in_User(request: Request, login_request: UserLogInSchema, db: Session= Depends(get_db_session)):
    return authenticate_user(request, login_request, db)



@router.get('/logout', status_code=status.HTTP_200_OK)
def log_out_user(request: Request):        
    return logout_user(request)



@router.get('/token', status_code=status.HTTP_200_OK)
def get_token(request: Request, db: Session= Depends(get_db_session)):        
    return get_access_token(request, db)


