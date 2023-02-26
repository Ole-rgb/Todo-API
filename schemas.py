from pydantic import BaseModel, Field
from typing import List
import datetime

class TodoBase(BaseModel):
    name: str 
    dueTo: datetime.datetime
    completed: bool
    description: str 
    importance: int 

class TodoCreate(TodoBase):
    pass


class Todo(TodoBase):
    id: int
    owner_id: int

    class Config: 
        orm_mode = True



#elements that will be the same reading and writing (password will be hashed, aka. not the same)
class UserBase(BaseModel):
    username: str 
    user_email: str                                         
    
#for security the pasword is not in the Basemodel
class UserCreate(UserBase):
    user_password: str 

#for reading from the api (pw excluded!)
class User(UserBase):
    id: int
    todos: List[Todo] = []
    
    class Config:
        orm_mode = True


