from fastapi import APIRouter, HTTPException,Depends,Path
from sqlalchemy.orm import Session
from typing import Annotated
from starlette import status
import models
from database import SessionLocal
from pydantic import BaseModel,Field
from .auth import get_current_user


router = APIRouter()



def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency= Annotated[Session , Depends(get_db)]
user_dependency= Annotated[dict , Depends(get_current_user)]