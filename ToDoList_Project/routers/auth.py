from fastapi import  APIRouter
from pydantic import BaseModel, EmailStr, Field
from models import Users

# if we use normal app initialization we need different port to run and
# it will run as different application so we are going to implement routing
# app = FastAPI()  


router = APIRouter()

class UserRequest(BaseModel):
    username : str = Field(min_length=3)
    email : EmailStr 
    first_name : str = Field(min_length=3)
    last_name :str = Field(min_length=3)
    password: str
    role:str

@router.get("/auth/")
async def get_user():

    return {'user': 'authenthicated'}


@router.post("/auth/createuser/")
async def create_user(create_user: UserRequest):

    # user_model = Users(**create_user.model_dump())
    # model dump() will not work since the request body have password and the db model have hashed password as key.
    #since the keys are different this will not work and we need to enter them one by one

    user_model = Users(
        email = create_user.email,
        username = create_user.username,
        hashed_password = create_user.password,
        first_name = create_user.first_name,
        last_name = create_user.last_name,
        role = create_user.role,
        is_active = True

    )


    return {user_model}