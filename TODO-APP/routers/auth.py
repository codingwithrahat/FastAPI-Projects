from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from RequestBody import UserRequest
from models import Users

from passlib.context import CryptContext
#pip install paslib
#pip install bcrypt==4.0.1

from sqlalchemy.orm import Session
from database import Sessionlocal
from typing import Annotated
from starlette import status

from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
#pip install python-multipart  (for form)
#OAuth2PasswordRequestForm - not a normal from , more secure

# OAuth2PasswordBearer tells FastAPI:
# This API uses Bearer token authentication.
# So Swagger shows the Authorize button.

from jose import jwt, JWTError
from datetime import timedelta, datetime, timezone
# datetime gives current date/time
# timedelta is used to add or subtract time
# timezone handles UTC or other time zones

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

#jwt need a secret key and a algorithm
Secret_Key = '2993fdb56fddc662acc3a0bf1eb9205c7060914d9b8268cd087a6bc3661d4034'
#anything i want
#random hexadecimal string genrate cmd - openssl rand -hex 32
Algorithm = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
# It is used to hash passwords and verify passwords securely.

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session ,Depends(get_db)]

class Token(BaseModel):
    access_token : str
    token_type : str


def authenticate_user(username : str, password : str, db):
    user = db.query(Users).filter(Users.username == username).first()

    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    
    return user


def create_acesss_token(username : str, user_id : int, role : str, expired_delta : timedelta):
    encode = {'sub' : username, 'id' : user_id, 'role' : role}    
    #create payload
    expires = datetime.now(timezone.utc) + expired_delta  
    encode.update({'exp' : expires})           
    # Add exp to payload; after this time the token will expire

    return jwt.encode(encode, Secret_Key, algorithm=Algorithm) 
    #create jwt token
    #header will generate automatic using algorithm
    #signature will generate using Secrect_key


async def get_current_user(token : Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, Secret_Key, algorithms=[Algorithm])
        username : str = payload.get('sub')
        user_id : int = payload.get('id')
        user_role : str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
        
        return {"username" : username, 'id' : user_id, 'user_role' : user_role}

    except JWTError: 
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db : db_dependency, create_user : UserRequest):

    #we can't use direct convert to dict and pass to User_model
    #cz password != hashed_password, it called manual mapping from pydantic model to SQLAlchemy model

    user_model = Users(
        email = create_user.email,
        username = create_user.username,
        first_name = create_user.first_name,
        last_name = create_user.last_name,
        role = create_user.role,
        hashed_password = bcrypt_context.hash(create_user.password),
        is_active = True
    )

    db.add(user_model)
    db.commit()



#response_model defines and validates the structure of the data your API returns.
#if i return any int value as token like 'access_token : 5
# it will raise an error (because it doesn’t match Token (str))

@router.post("/token", response_model=Token)
async def login_for_acess_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db : db_dependency):

    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
    

    token = create_acesss_token(user.username, user.id, user.role, timedelta(minutes=20))
    return {'access_token' : token, "token_type" : 'bearer'}
    # Whoever bears (has/carries) the token can use it.
    