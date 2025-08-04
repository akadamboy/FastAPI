from typing import Optional
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
    
    id : Optional[int] = Field(description="id is not needed to create ", default=None) # no need to pass id in request body
    title : str = Field(min_length=3)
    author: str = Field(min_length=3)
    description: str = Field(min_length=4, max_length=100)
    rating: int = Field(gt=-1 , le=5)

    # giving default values to the fields using pydantic config  
    # class_config was in old version of pydantic new version use model_config
    #since we didn't give id in json_schema_extra: exampl: it will not show the id while we enter data
    model_config = {
        "json_schema_extra" :{
            "example": {
                "title" : "book name 1",
                "author" : "author 2",
                "description" : "this is a book about dragons",
                "rating" : 4
            }
        }

    }


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
    
    BOOKS.append(set_book_id(new_book))
    return f"{new_book} added"

# function to get book by id
@app.get("/book/{book_id}")
async def read_book(book_id: int):

    for book in BOOKS:
        if book.id == book_id:
            return book  
    return  "book not found"

#code to fech book by raing
@app.get("/book/")
async def read_book_by_rating(book_rating :int):
    book_by_rating=[]
    for book in BOOKS:
        if book.rating == book_rating:
            book_by_rating.append(book)
    return book_by_rating if len(book_by_rating) >0 else f"no book with rating {book_rating}"

@app.put("/book/update_book")
async def update_book(book : BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id :
            BOOKS[i] = book
    return "book updated"

@app.delete("/book/delete")
async def delete_book(id : int):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == id :
            BOOKS.pop(i)
            break
        else:
            return f"no book with id {id}"


def set_book_id(book:Book): #function to set the book id 

    # book.id = 1 if len(BOOKS) == 0 else  BOOKS[-1].id + 1 # oneliner to set id
    if (len(BOOKS) > 0):
        book.id = BOOKS[-1].id  + 1
    else:
        book.id = 1
    return book