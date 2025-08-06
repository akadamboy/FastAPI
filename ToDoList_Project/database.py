from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base




SQLALCHEMY_DATABASE_URL = "sqlite:///./todo.db" #sql lite database url

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False}) 
#created engine which is used to communicate with the database check_same_thread false can help use db using multiple threads
# engine define which database to connect

SessionLocal = sessionmaker(autoflush=False, autocommit = False, bind=engine)
#session uses the engine and it is an interface for handling python objects ans sync them with database rows
#provides a transactional context to read/write objects.

Base = declarative_base()
#holds metadata about all your mapped classess
#uses the engine to create all tables defined in classes inheriting from Base.