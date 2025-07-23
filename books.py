from fastapi import FastAPI

app = FastAPI()


BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]



@app.get("/") # home page 
async def home():
    return {'home page'}

@app.get("/welcome") #welcome page
async def greet():
    return {'Hi Good morning!'}

@app.get("/books") #return all the books
async def read_all_books():
    return BOOKS 

# passing dynamic parameter through URL

@app.get("/books/{book_name}")
async def read_book_by_name(book_name):
    book_name = book_name

    #we can write the retun statement in multiple ways
    # return ( f"book name is {book_name}" )  # using fstriing
    # return f"book name is {book_name}"   #fstring
    # return "book name is "+book_name
    return {"book name" :book_name} # returns a dictionary object

