import token

from fastapi import HTTPException, status, Request, BackgroundTasks
from src.user.dtos import UserSchema, LoginSchema
from sqlalchemy.orm import Session
from src.user.models import UserModel
from pwdlib import PasswordHash
from src.utils.settings import Settings
from datetime import datetime, timedelta
import jwt 
from jwt.exceptions import InvalidTokenError
from src.utils.mail import send_email


password_hash = PasswordHash.recommended()

def get_password_hash(password):
    return password_hash.hash(password)

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)



async def register(body:UserSchema, db:Session,bg_task:BackgroundTasks):
    is_user = db.query(UserModel).filter(UserModel.username==body.username).first()
    if is_user :
        raise HTTPException(status_code=400, detail = "user name already exists..")
    
    is_user = db.query(UserModel).filter(UserModel.email==body.email).first()
    if is_user :
            raise HTTPException(status_code=400, detail = "email already exists..")

    hash_password = get_password_hash(body.password)

    new_user = UserModel(
        name = body.name,
        username = body.username,
        hash_password = hash_password,
        email = body.email
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)


    ##send emial confirmation
   
    bg_task.add_task(send_email,[new_user.email])
    
    return new_user

    

   
    ##1. check username validation
    ##2. check email validation

def login_user(body:LoginSchema, db:Session):
    user = db.query(UserModel).filter(UserModel.username==body.username).first()
    if not user:
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You Entered Invalid username or password")

    if not verify_password(body.password, user.hash_password):
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You Entered Invalid username or password")

    exp_time = datetime.now() + timedelta(minutes=Settings.EXP_TIME)
    print(exp_time)
    token = jwt.encode({"id": user.id, "exp": exp_time.timestamp()}, Settings.SECRET_KEY, Settings.ALGORITHM)


    return ("token:", token)

## token send - headers

def is_authenticated(request:Request, db:Session):
    try:
        token = request.headers.get("Authorization")
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not unauthorized")
        token = token.split(" ")[-1]

        data = jwt.decode(token, Settings.SECRET_KEY, Settings.ALGORITHM)
        user_id = data.get("id")

    
        user = db.query(UserModel).filter(UserModel.id==user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not unauthorized")
    

        return user
    
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not unauthorized")

