from fastapi import FastAPI, Body, Path, Query, HTTPException
from books import Book
from bookModel import BookModel
from starlette import status
#use it when we want to customize success responses

app = FastAPI()

Books = [
    Book(1, 'cse', 'rahat', 'nice book', 5, 2012),
    Book(2, 'eee', 'rakib', 'awesome book', 4, 2013),
    Book(3, 'me', 'rahat', 'very nice', 3, 2013),
    Book(4, 'ipe', 'sarawer', 'nice', 2, 2014),
    Book(5, 'ce', 'rahat', 'awesome', 1, 2015),
    Book(6, 'ict', 'rakib', 'very nice book', 5, 2016)
]


#200 default status code , means sucessfull
@app.get("/books", status_code=status.HTTP_200_OK)
async def all_books():
    return Books

# Data validation path parameter Path()
@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def id_book(book_id : int = Path(gt=0)):
    for i in range(len(Books)):
        if Books[i].id == book_id :
            return Books[i]
    raise HTTPException(status_code=404, detail='item not found')     
#404 error means the resource is not found

    
# Data validation path parameter Query()
@app.get("/books/", status_code=status.HTTP_200_OK)
async def rating_book(book_rat : int = Query(gt=1, lt=6)):
    book_list = []
    for i in range(len(Books)):
        if Books[i].rating == book_rat :
            book_list.append(Books[i])
    
    return book_list


# 201 means created a data, return null response body
@app.post("/create_book", status_code=status.HTTP_201_CREATED)
async def create_book(new_book : BookModel):
    conv_book = Book(**new_book.dict())
    Books.append(find_id(conv_book))


def find_id(book : Book):
    if len(Books) > 0:
        book.id = Books[-1].id + 1  # -1 means last index
    else:
        book.id = 1
    
    return book


#204 means req is succesful but there is no content to return, no body will show
@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
def update_book(book : BookModel):
    f = False
    for i in range(len(Books)):
        if Books[i].id == book.id:            
            Books[i] = Book(**book.dict())
            f = True
    
    if not f:
        raise HTTPException(status_code=404, detail='Item not found')



@app.delete("/books/delete_book/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book_id(book_id : int = Path(gt=0)):
    f = False
    for i in range(len(Books)):
        if Books[i].id == book_id:
            Books.pop(i)
            f = True
            break
    if not f:
        raise HTTPException(status_code=404, detail='Item not found')
            

@app.get("/books/published_date/")
async def date(pub : int):
    book_list = []
    for i in range(len(Books)):
        if Books[i].published_date == pub:
            book_list.append(Books[i])    
    return book_list

