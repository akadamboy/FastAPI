from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import  APIRouter, Depends, status
from pydantic import BaseModel, EmailStr, Field
from database import SessionLocal
from models import Users
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt

# if we use normal app initialization we need different port to run and
# it will run as different application so we are going to implement routing
# app = FastAPI()  


router = APIRouter()

SECRET_KEY ='1280b4cbcc3b73c4891785d9adced5102421d5d9d4f0e04b3d6c31b58d9ff8a7'
#i used "openssl rand -hex 32" this command to generate this random string
ALGORITHM = 'HS256' 



bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')

class UserRequest(BaseModel):
    username : str = Field(min_length=3)
    email : EmailStr 
    first_name : str = Field(min_length=3)
    last_name :str
    password: str
    role:str

def get_db():
    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()

db_dependency = Annotated[ Session, Depends(get_db) ]


# this function verifies the user name pand password entered
def authenticate_user(username:str, password: str, db:db_dependency):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def generate_token(username: str, user_id: int, expire_time: timedelta):

    encode_data = {'sub': username,
              'id': user_id}
    

    # expire = datetime.utcnow() -> this one is depricated
    expire = datetime.now(timezone.utc) + expire_time
    encode_data.update({'exp':expire})
    token = jwt.encode(encode_data, SECRET_KEY, algorithm = ALGORITHM)
    return token



@router.get("/auth/")
async def get_user():

    return {'user': 'authenthicated'}


@router.post("/auth/createuser/", status_code= status.HTTP_201_CREATED)
async def create_user(create_user: UserRequest, db :db_dependency):

    # user_model = Users(**create_user.model_dump())
    # model dump() will not work since the request body have password and the db model have hashed password as key.
    #since the keys are different this will not work and we need to enter them one by one

    user_model = Users(
        first_name = create_user.first_name,
        last_name = create_user.last_name,
        email = create_user.email,
        username = create_user.username,
        hashed_password = bcrypt_context.hash(create_user.password),
        role = create_user.role,
        is_active = True

    )
    db.add(user_model)
    db.commit()


    return {user_model}


@router.get("/auth/get_all/", status_code=status.HTTP_200_OK)
def get_all_user(db:db_dependency):
    return db.query(Users).all()


@router.post("/token")
async def login_for_toker(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                          db : db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return 'username and password doest match'
    token = generate_token(user.username, user.id, timedelta(minutes=20))
    return token

