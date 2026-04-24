from fastapi import APIRouter, Depends, HTTPException, Path
from database import Sessionlocal
from typing import  Annotated
from sqlalchemy.orm import Session
from models import Todos
from starlette import status
from RequestBody import TodoRequest

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


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(db : db_dependency):
    return db.query(Todos).all() 


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(db : db_dependency, todo_id : int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail='todo not found.')



@router.post("/todo")
async def create_todo(db : db_dependency, todo_req : TodoRequest):
    todo_model = Todos(**todo_req.dict())

    db.add(todo_model)
    db.commit()




@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db : db_dependency, todo_req : TodoRequest, todo_id : int = Path(gt=0)):

    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
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
async def delete_todo(db : db_dependency, todo_req : TodoRequest, todo_id : int = Path(gt=0)):

    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.query(Todos).filter(todo_id == Todos.id).delete()

    db.commit()