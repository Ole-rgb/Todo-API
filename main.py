from fastapi import FastAPI, Path, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import List
import datetime
import json

import models, schemas, crud
from database import engine, SessionLocal 

#TODO add layer of protection so that i can only see my todos ! (accessToken?!)

#creates the db-table
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#configure CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
   db = SessionLocal()
   try:
       yield db
   finally:
       db.close()

#reads all todos
@app.get("/todos/", response_model=List[schemas.Todo])
def read_todos(db:Session=Depends(get_db)):
    return crud.get_todos(db)

#only register a user that has a unique username 
@app.post("/users/", response_model=schemas.User)
def create_user(user:schemas.UserCreate,db:Session=Depends(get_db)):
    #check if the user already exists 
    created_user = crud.create_user(db=db, user=user)
    if created_user is None:
        raise HTTPException(status_code=404, detail="Username already exists")
    return created_user


#reads all users
@app.get("/users", response_model=List[schemas.User])
def read_users(db:Session=Depends(get_db)):
    users=crud.get_users(db)
    return users

#reads a user
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db:Session=Depends(get_db)):
    db_user=crud.get_user(user_id=user_id,db=db)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


#creates a todo for a user
@app.post("/users/{user_id}/todo/", response_model=schemas.Todo)
def create_todo_for_user(user_id:int, todo:schemas.TodoCreate, db:Session=Depends(get_db)):
    return crud.create_user_todo(todo=todo, user_id=user_id, db=db)


#delete a todo soecific to a user
@app.delete("/users/{user_id}/todo", response_model=schemas.Todo)
def delete_user_todo(user_id: int, todo_id:int, db: Session = Depends(get_db)):
    deleted_todo = crud.delete_user_todo(user_id=user_id, todo_id=todo_id, db=db)
    if deleted_todo:
        return deleted_todo 
    else:
        raise HTTPException(status_code=404, detail="User todo not found")
    
    
##############################################################################################################################

@app.post("/auth", response_model={})
def login_user(user:schemas.UserCreate, db:Session=Depends(get_db)):
    if crud.user_exists(user, db):
        #create Tokens 
        return 
    raise HTTPException(status_code=401, detail="User not in database")