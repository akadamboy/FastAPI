from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, Path, status
from database import SessionLocal, engine
from sqlalchemy.orm import Session
import models
from models import Todos


app = FastAPI()

models.Base.metadata.create_all(bind= engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)] # assigning Annotated to a variable


@app.get("/", status_code= status.HTTP_200_OK)
# async def get_all(db: Annotated[Session, Depends(get_db)]): #we can give the Annotated type here directly or we can assign it to a variable
async def get_all(db: db_dependency):
    return db.query(Todos).all()
    

@app.get("/todo/{todo_id}", status_code= status.HTTP_200_OK)
async def get_todo_by_id(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="todo id not found")