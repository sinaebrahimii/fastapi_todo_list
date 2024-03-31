from fastapi import FastAPI, HTTPException,Depends,Path
from sqlalchemy.orm import Session 
from typing import Annotated
import models
from database import SessionLocal, engine
from starlette import status
from pydantic import BaseModel,Field
from routers import auth,todos

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)