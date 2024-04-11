from fastapi import APIRouter, HTTPException,Depends,Path
from sqlalchemy.orm import Session
from typing import Annotated
from starlette import status
from models import Users
from database import SessionLocal
from pydantic import BaseModel,Field
from .auth import get_current_user


router = APIRouter(prefix='/users', tags=['users'])



def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency= Annotated[Session , Depends(get_db)]
user_dependency= Annotated[dict , Depends(get_current_user)]

class ChangePasswordRequest(BaseModel):
    old_password : str
    new_password : str
    new_password_rpt:str

@router.get('',status_code=status.HTTP_200_OK)
async def get_user(user:user_dependency,db:db_dependency):
    if user is None :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Autuntecation failed.')
    user=db.query(Users).filter(Users.id==user.get('id')).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    return user
    
@router.post('/changepassword',status_code=status.HTTP_201_CREATED)
async def change_password(user:user_dependency,db:db_dependency):
    pass