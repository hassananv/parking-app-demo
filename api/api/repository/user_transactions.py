from fastapi import status, HTTPException
from models.user_model import UserModel
from sqlalchemy.orm.session import Session
from sqlalchemy import exc
from api.schemas.user_schema import UserRegisterSchema, UserUpdateSchema
from api.repository.auth_transactions import get_password_hash, verify_password

MIN_PASSWORD_LENGTH = 5

def get_user(email, db: Session):
        
    user = db.query(UserModel).filter( UserModel.email==email).first()
    
    if not user:
        raise HTTPException(status_code=404, detail=f"User is not available.")
     
    return user


def create_user(request: UserRegisterSchema, db: Session):

    try:
        user_request = request.dict()
        password = user_request["password"]

        if 'password' in user_request and user_request['password'] and len(user_request['password'])<MIN_PASSWORD_LENGTH:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Weak Password!")

        user_request["password"] = get_password_hash(password)
        user_request["email"] = user_request["email"].lower()

        new_user = UserModel(**user_request)       
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user.id

    except exc.SQLAlchemyError as e: 
        if e.__dict__ and 'orig' in e.__dict__:
            error_msg = str(e.__dict__['orig'])
        else:
            error_msg = str(e)
        stat = status.HTTP_400_BAD_REQUEST
        if "duplicate" in error_msg or "already exists" in error_msg:
            stat = status.HTTP_409_CONFLICT
        err = error_msg.split("DETAIL")
        if len(err)>1:
           error_msg =  err[1]
        raise HTTPException(status_code=stat, detail=error_msg)



def modify_user(request:UserUpdateSchema, db, email):
    user_request = request.dict()
    user_email = user_request['email']    

    if email != user_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User Email should not be changed!")

    user_query = db.query(UserModel).filter( UserModel.email==user_email)
    user = user_query.first()

    if not user:
        raise HTTPException(status_code=404, detail=f"User is not available.")


    if 'old_password' in user_request and user_request['old_password']:
        old_password = user_request['old_password']

        if not verify_password(old_password, user.password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Old Password Error!")
        
    del user_request['old_password']

    if 'password' in user_request and user_request['password'] and len(user_request['password'])<MIN_PASSWORD_LENGTH:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Weak Password!")

    if 'password' in user_request and not user_request['password']:
        del user_request['password']
    elif 'password' in user_request:
        password = user_request["password"]
        user_request["password"] = get_password_hash(password)
    
    user_query.update(user_request)
    db.commit()

    return "success"



