from fastapi import APIRouter, Depends, HTTPException, Path
from database import Sessionlocal
from typing import  Annotated
from sqlalchemy.orm import Session
from models import Todos
from starlette import status
from RequestBody import TodoRequest

from .auth import get_current_user
#This will NOT work unless the folder is a package

router = APIRouter(
    tags=['todos']
)


def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session ,Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user : user_dependency, db : db_dependency):

    if user is None:
        raise HTTPException(status_code=401, detail = 'Authentication Failed')

    return db.query(Todos).filter(user.get('id') == Todos.owner_id).all()


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(user : user_dependency, db : db_dependency, todo_id : int = Path(gt=0)):

    if user is None:
        raise HTTPException(status_code=401, detail = 'Authentication Failed')

    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id  == user.get('id')).first()

    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail='todo not found.')



@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(user : user_dependency, db : db_dependency, todo_req : TodoRequest):

    if user is None:
        raise HTTPException(status_code=401, detail = 'Authentication Failed')


    todo_model = Todos(**todo_req.dict(), owner_id = user.get('id'))

    db.add(todo_model)
    db.commit()




@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user : user_dependency, db : db_dependency, todo_req : TodoRequest, todo_id : int = Path(gt=0)):

    if user is None:
        raise HTTPException(status_code=401, detail = 'Authentication Failed')

    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    # it also act like call by reference

    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    todo_model.title = todo_req.title
    todo_model.description = todo_req.description
    todo_model.priority = todo_req.priority
    todo_model.complete = todo_req.complete

    # db.add(todo_model)  #no need (call by ref) 
    db.commit()




@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user : user_dependency, db : db_dependency, todo_id : int = Path(gt=0)):

    if user is None:
        raise HTTPException(status_code=401, detail = 'Authentication Failed')

    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.query(Todos).filter(todo_id == Todos.id).filter(Todos.owner_id == user.get('id')).delete()
    db.commit()