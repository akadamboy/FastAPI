from typing import Annotated
from fastapi import FastAPI, Depends
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


@app.get("/")
# async def get_all(db: Annotated[Session, Depends(get_db)]): #we can give the Annotated type here directly or we can assign it to a variable
async def get_all(db: db_dependency):
    return db.query(Todos).all()
    