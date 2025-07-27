class Book():
    bookId:int
    title:str
    author:str
    description:str
    rating:int
    
    def __init__(self,bookId,title,author,description,rating):
        self.bookId = bookId
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
    
