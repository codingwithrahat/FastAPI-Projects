from fastapi import APIRouter, Depends, HTTPException, Path
from database import Sessionlocal
from typing import  Annotated
from sqlalchemy.orm import Session
from models import Todos, Users
from starlette import status
from RequestBody import TodoRequest

from .auth import get_current_user
#This will NOT work unless the folder is a package

router = APIRouter(
    prefix='/users',
    tags=['users']
)


def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session ,Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/todos", status_code=status.HTTP_200_OK)
async def your_info(user : user_dependency, db : db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authetication Failed')
    
    return db.query(Users).filter(Users.id == user.get('id')).first()
