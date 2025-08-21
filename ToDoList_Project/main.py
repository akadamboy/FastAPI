from typing import Annotated, Optional
from fastapi import FastAPI, Depends, HTTPException, Path, status
from pydantic import BaseModel, Field
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

#creating a class to verify the data coming from post request body


class TodoRequest(BaseModel):
    # id : Optional[int]  no need to add id here cause sql alchemy will take care of this
    title : str = Field(min_length=3)
    description : str = Field(min_length=5, max_length= 100)
    priority : int = Field(gt=0, le=5)
    complete_status : bool = Field(default= False)






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


@app.post("/todo/create", status_code = status.HTTP_201_CREATED)
async def create_todo(todo_item: TodoRequest, db: db_dependency): #take data from request body and create database session

    todo_model = Todos(**todo_item.model_dump())  #map the values to the todo class variables and create a data model to add to the database
    db.add(todo_model) #insert the model to database
    db.commit() #commits the insert


@app.put("/todo/update/{todo_id}", status_code= status.HTTP_204_NO_CONTENT)
async def update_todo(db: db_dependency, 
                      #todo_id: int = Path(gt=0), # Can not give path validation above the request body will give error
                      todo_request: TodoRequest,
                      todo_id: int = Path(gt=0)):

    todo_model =  db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="item not found in db")
    
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete_status = todo_request.complete_status

    db.add(todo_model)
    db.commit()
    return "update success"


@app.delete("/todo/delete/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id:int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404 , detail="todo with id not found in db")
    # db.query(Todos).filter(Todos.id == todo_id).delete() 
    db.delete(todo_model)
    db.commit()

    
    
        
