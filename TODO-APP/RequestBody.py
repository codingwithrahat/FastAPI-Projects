from pydantic import BaseModel, Field


class UserRequest(BaseModel):
    username : str
    email : str
    first_name : str
    last_name : str
    password : str
    role : str

    

class TodoRequest(BaseModel):
    
    title : str = Field(min_length=3)
    description : str = Field(min_length=3, max_length=100)
    priority : int  = Field(gt=0, lt=6)
    complete : bool 


