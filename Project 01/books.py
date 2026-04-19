from fastapi import FastAPI, Body

app = FastAPI()

books = [
    {"title": "t1", "author": "a1", "des": "d1"},
    {"title": "t2", "author": "a2", "des": "d1"},
    {"title": "t3", "author": "a1", "des": "d1"}
]

@app.get("/all_books")
async def all_book():
    return books


@app.get("/books/one")
async def id_book():
    return books[0] 

#here order matter before "/books/one" then path
#path parameter
@app.get("/books/{book_name}")
async def id_book_path(book_name : str):
    for i in range(len(books)):
        if books[i]["title"].casefold() == book_name.casefold() :
            return books[i]

#query parameter
@app.get("/books")
async def id_book_query(book_name : str):
    for i in range(len(books)):
        if books[i]["title"].casefold() == book_name.casefold() :
            return books[i]

# path parameter + query parameter
@app.get("/books/filter/{cat}")
async def read_all_books(cat :str, author: str):

    l = []
    for i in books:
        if i.get("title").casefold() == cat.casefold() and i.get("author").casefold() == author.casefold():
            l.append(i)
    return l;


@app.post("/add_book")
async def add_book(new_book=Body()):
    books.append(new_book)


@app.put("/update_books")
async def update_book(up=Body()):
    for i in range(len(books)):
        if books[i]["title"].casefold() == up["title"].casefold():
            books[i] = up


@app.delete("/delete_books/{books_title}")
async def delet_book(books_title : str):
    for i in range(len(books)):
        if books[i].get("title").casefold() == books_title.casefold():
            books.pop(i)
            break