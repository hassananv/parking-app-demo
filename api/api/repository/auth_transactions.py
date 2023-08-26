from fastapi import status, HTTPException, Request
from models.user_model import UserModel
from sqlalchemy.orm.session import Session
from core.JWTtoken import create_access_token
from datetime import datetime
from passlib.context import CryptContext
from api.schemas.user_schema import  UserLogInSchema

TOKEN_EXPIRATION_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)



def authenticate_user(request: Request, login_request: UserLogInSchema, db: Session):

    clear_cookies(request)

    user_query = db.query(UserModel).filter( UserModel.email==login_request.email.lower())
    user = user_query.first()
    
    if not user:
        raise HTTPException(status_code=404, detail=f"User is not available.")
    
    if verify_password(login_request.password, user.password):
        
        request.session["user_email"] = user.email
        user_query.update({"last_login": datetime.now()})
        db.commit()
        return "success"
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User/Password is invalid.")




def logout_user(request: Request):
    clear_cookies(request)
    return "success"



def clear_cookies(request: Request):
    request.session["user_email"] = None      
    request.session.clear()



def get_access_token(request: Request, db: Session):

    login_response = {"access_token": None, "token_type": "bearer"}
        
    if("user_email" in request.session and request.session["user_email"] is not None):
        
        email = request.session["user_email"]
        user = db.query(UserModel).filter( UserModel.email==email).first()
        
        if ((not user) or (login_expired(user.last_login, TOKEN_EXPIRATION_MINUTES))):
            clear_cookies(request)
            return login_response

        access_token = create_access_token(data={"sub": user.email, "id":user.id})              
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        return login_response

def login_expired(last_login, expiration_minutes):
    current_time = datetime.now(last_login.tzinfo)
    time_diff = current_time-last_login       
    minutes_diff = (time_diff.seconds / 60)-expiration_minutes
    return minutes_diff > 0