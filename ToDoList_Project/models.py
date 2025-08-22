#model file used to define the tables in the database.

from database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String


class Todos(Base):  # class inherits the base we declared in the database.py file using declarative_base()
    __tablename__ = 'todos' 

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete_status = Column(Boolean, default= False)
    owner_id = Column(Integer, ForeignKey("users.id"))


class Users(Base):

    __tablename__ = 'users'

    id = Column(Integer,  primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique= True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default = True)
    role = Column(String)
    

