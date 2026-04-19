from fastapi import FastAPI

app = FastAPI()

books = [
    {'title' : 'cse', 'author' : 'rahat'},
    {'title' : 'eee', 'author' : 'rakib'},
    {'title' : 'math', 'author' : 'sarawer'},
    {'title' : 'english', 'author' : 'rahat'},
    {'title' : 'bangla', 'author' : 'rahat'},
]


# using query parametter
#url wil be - /author_books_querystyle?searchauthor=rahat
@app.get("/author_books/")
async def author_book_query(search_author : str):
    author_list = []
    for i in range(len(books)):
        if books[i].get('author').casefold() == search_author.casefold():
            author_list.append(books[i])
    return author_list



# using path parameter
# url will be - /author/rahat
@app.get("/author_books/{search_author}")
async def author_book_path(search_author : str):
    author_list = []
    for i in range(len(books)):
        if books[i].get('author').casefold() == search_author.casefold():
            author_list.append(books[i])
    return author_list



#using both
#ptah for find author and query for find the title
@app.get("/author_filter/{search_author}")
async def author_title(search_author : str, search_title : str):
    for book in books:
        if book.get('author').casefold() == search_author.casefold() and book.get('title').casefold() == search_title.casefold():
            return book









