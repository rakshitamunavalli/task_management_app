from fastapi import Request, HTTPException, status,Depends
from src.utils.settings import Settings
from sqlalchemy.orm import Session
import jwt
from jwt.exceptions import InvalidTokenError
from src.user.models import UserModel
from src.utils.db import get_db




def is_authenticated(request:Request, db:Session=Depends(get_db)):
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

