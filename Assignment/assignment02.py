from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

class Book:
    id : int
    title : str
    author : str
    description : str
    rating : int
    published_date : int

    def __init__(self , id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookModel(BaseModel):
    id : Optional[int] = Field(description='id is not neeeded on create', default = None)
    title : str = Field(min_length=3, max_length=20)
    author : str = Field(min_length=1)
    description : str = Field(min_length=1, max_length=100)
    rating : int = Field(gt = 0, lt = 6)   #1 to 5
    published_date : int = Field(ge=1999, le=2030)

    model_config = {
        "json_schema_extra" : {
            "example" : {
                "title" : "A new book",
                "author" : "rahat",
                "description" : "des 2",
                "rating" : 5,
                "published_date" : 2012

            }
        }
    }

Books = [
    Book(1, 'cse', 'rahat', 'nice book', 5, 2012),
    Book(2, 'eee', 'rakib', 'awesome book', 4, 2013),
    Book(3, 'me', 'rahat', 'very nice', 3, 2014),
    Book(4, 'ipe', 'sarawer', 'nice', 2, 2015),
    Book(5, 'ce', 'rahat', 'awesome', 1, 2016),
    Book(6, 'ict', 'rakib', 'very nice book', 5, 2017)
]

@app.get("/books")
async def all_books():
    return Books

@app.get("/books/{book_id}")
async def id_book(book_id : int):
    for i in range(len(Books)):
        if Books[i].id == book_id :
            return Books[i]

    

@app.get("/books/")
async def rating_book(book_rat : int):
    book_list = []
    for i in range(len(Books)):
        if Books[i].rating == book_rat :
            book_list.append(Books[i])
    
    return book_list



@app.post("/create_book")
async def create_book(new_book : BookModel):
    conv_book = Book(**new_book.dict())
    Books.append(find_id(conv_book))


def find_id(book : Book):
    if len(Books) > 0:
        book.id = Books[-1].id + 1  # -1 means last index
    else:
        book.id = 1
    
    return book


@app.put("/books/update_book")
def update_book(book : BookModel):
    for i in range(len(Books)):
        if Books[i].id == book.id:            
            Books[i] = Book(**book.model_dump())


@app.delete("/books/delete_book/{book_id}")
async def delete_book_id(book_id : int):
    for i in range(len(Books)):
        if Books[i].id == book_id:
            Books.pop(i)
            break


@app.get("/books/published_date/")
async def date(pub : int):
    book_list = []
    for i in range(len(Books)):
        if Books[i].published_date == pub:
            book_list.append(Books[i])    
    return book_list
