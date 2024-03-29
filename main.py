from fastapi import FastAPI, HTTPException,Depends,Path
from sqlalchemy.orm import Session 
from typing import Annotated
import models
from database import SessionLocal, engine
from starlette import status
from pydantic import BaseModel,Field

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency= Annotated[Session , Depends(get_db)]

class TodoRequest (BaseModel):
    title:str = Field(min_length=3)
    description:str =Field(min_length=3,max_length=100)
    priority : int =Field(gt=0,lt=6)
    complete: bool

@app.get("/",status_code=status.HTTP_200_OK)
async def read_all(db :db_dependency ):
    if db.query(models.Todos).all() is not None:
        return db.query(models.Todos).all()
    raise HTTPException(status_code=404,detail="Todo not found")

@app.get("/todo/{todo_id}",status_code=status.HTTP_200_OK)
async def read_todo(db:db_dependency,todo_id:int=Path(gt=0)):
  todo_model=  db.query(models.Todos).filter(models.Todos.id ==todo_id).first()
  if todo_model is not None:
      return todo_model
  raise HTTPException(status_code=404,detail="بچو کره دو")

@app.post("/todos",status_code=status.HTTP_201_CREATED)
async def create_todo(db:db_dependency,todo_request:TodoRequest):
    todo_model=models.Todos(**todo_request.model_dump())
    db.add(todo_model)
    db.commit()
    return "model created"
@app.put("/todos/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async  def update_todo(db:db_dependency,todo_request:TodoRequest ,todo_id:int=Path(gt=0)):
    todo_model=db.query(models.Todos).filter(models.Todos.id ==todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404,detail="Todo not found")
    todo_model.title=todo_request.title
    todo_model.description=todo_request.description
    todo_model.complete=todo_request.complete
    todo_model.priority=todo_request.priority
    db.add(todo_model)
    db.commit()
    return "todo updated"

@app.delete("/todos/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db:db_dependency, todo_id:int=Path(gt=0)):
    todo_model=db.query(models.Todos).filter(models.Todos.id ==todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404,detail="Todo not found")
    db.query(models.Todos).filter(models.Todos.id==todo_id).delete()
    db.commit()