from fastapi import FastAPI, Body
from books import Book
from bookModel import BookModel

app = FastAPI()

Books = [
    Book(1, 'cse', 'rahat', 'nice book', 5, 2012),
    Book(2, 'eee', 'rakib', 'awesome book', 4, 2013),
    Book(3, 'me', 'rahat', 'very nice', 3, 2013),
    Book(4, 'ipe', 'sarawer', 'nice', 2, 2014),
    Book(5, 'ce', 'rahat', 'awesome', 1, 2015),
    Book(6, 'ict', 'rakib', 'very nice book', 5, 2016)
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
            Books[i] = Book(**book.dict())


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

