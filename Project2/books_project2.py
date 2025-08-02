from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Book:
    
    def __init__ (self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating

class BookRequest(BaseModel):    #this object inherit BaseModel and varify the data coming from body
    
    id : int 
    title : str = Field(min_length=3)
    author: str = Field(min_length=3)
    description: str = Field(min_length=4, max_length=100)
    rating: int = Field(gt=-1 , le=5)


BOOKS = [Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5),
    Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!', 5),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1)
]


@app.get("/books")
async def books_home():

    return BOOKS

#--------Introducing Pydantics ------#

# Library used for data modeling, data parsing and for efficient error handiling. 
# We can use it for data validation



# @app.post("/book/create")
# async def create_book(new_book = Body()):  #the data coming from the body is not validated before inserting

#     BOOKS.append(new_book)

#     return "book created"


@app.post("/book/create")
async def create_book(new_book :BookRequest):
    #new_book = Book(**new_book.dict())    #convert the request to Book object instead of BookRequest object
                                           # the .dict() is used in Pydantic V1 and is depricated

    new_book = Book(**new_book.model_dump()) # model_dump() is the new .dict() in Pydantic V2   
    # type of new book change from BookRequest to Book

    BOOKS.append(new_book)
    return f"{new_book} added"

