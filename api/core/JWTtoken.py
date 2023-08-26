
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from starlette.requests import Request
from core.config import settings
from api.schemas.token_schema import TokenDataSchema

SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt




def verify_token(token: str, credentials_exception, request: Request):
    
    if token is None:
        # print("_________Internal_Token_Not_Found_________")
        raise credentials_exception
    
    if( "user_email" not in request.session):
        # print("_________Internal_Token_User_Email_Not_Found_________")
        raise credentials_exception

    user_email = request.session["user_email"]

    try:        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])       

        email: str = payload.get("sub")
        user_id: int = payload.get("id")
        if email is None or user_email is None or email != user_email:
            raise credentials_exception

        token_data = TokenDataSchema(email=email)

        return { "email":email, "id":user_id}

    except jwt.ExpiredSignatureError:
        # print("_____________________Internal_Token_Signature_Error___")
        return {"email":None, "id":None}

    except jwt.JWTClaimsError:
        # print("_____________________Internal_Token_CLAIM_Error___")
        raise credentials_exception

    except JWTError:
        # print("_____________________Internal_Token_Error___")
        raise credentials_exception
