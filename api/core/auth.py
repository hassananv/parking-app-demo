from fastapi import Request, status, HTTPException, Depends
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer
from core import JWTtoken

token_bearer_schema = HTTPBearer()




def logged_in_user(request: Request,  token: HTTPAuthorizationCredentials = Depends(token_bearer_schema)):
    
    if("user_email" in request.session and request.session["user_email"] is not None)or ("oidc_user_email" in request.session and request.session["oidc_user_email"] is not None):
        return verify_user(request, token)        
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Unauthorized user.")
    
    



def verify_user(request: Request, token: HTTPAuthorizationCredentials):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    user = JWTtoken.verify_token(token.credentials, credentials_exception, request)

    if (("email" not in user) or (user["email"] is None )):
        raise credentials_exception    
    else:
        return user