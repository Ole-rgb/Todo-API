from fastapi import FastAPI, Path, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import Field
from sqlalchemy.orm import Session
from typing import List, Union

import models, schemas, crud
from database import engine, SessionLocal 
import auth.jwt_handler as JWTHandler
from auth.jwt_bearer import JWTBearer

#TODO add layer of protection so that i can only see my todos ! (accessToken?!)
#TODO how can you only access your own Todos? (accessToken should handle that somehow)

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


#FOR ADMIN
############################################################################################################################################

#READ ALL TODOs 
#TODO will be removed later (only for troubleshooting or the admin?)
@app.get("/todos/", response_model=List[schemas.Todo], tags=["ADMIN"])
def read_todos(db:Session=Depends(get_db)):
    return crud.get_todos(db)

#READ ALL USERS 
#TODO will be removed later (only for troubleshooting or the admin?)
@app.get("/users", response_model=List[schemas.User], tags=["ADMIN"])
def read_users(db:Session=Depends(get_db)):
    users=crud.get_users(db)
    return users

#READ A USER  (via ID)
@app.get("/users/{user_id}", response_model=schemas.User, tags=["ADMIN"])
def read_user(user_id: int, db:Session=Depends(get_db)):
    db_user=crud.get_user_by_id(user_id=user_id,db=db)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

#READ ALL ToDos FROM ONE USER (via ID)
@app.get("/users/{user_id}/todo/" , response_model=List[schemas.Todo], tags=["ADMIN"])
def read_todos_from_user(user_id:int, db:Session=Depends(get_db)):
    return crud.get_user_todos_by_id(user_id=user_id,db=db)

# CREATE ToDo FOR USER
@app.post("/users/{user_id}/todo/", response_model=schemas.Todo, tags=["ADMIN"])
def create_todo_for_user(user_id:int, todo:schemas.TodoCreate, db:Session=Depends(get_db)):
    return crud.create_user_todo(todo=todo, user_id=user_id, db=db)

# DELETE A ToDo FROM A USERID
@app.delete("/users/{user_id}/todo", response_model=schemas.Todo, tags=["ADMIN"])
def delete_user_todo(user_id: int, todo_id:int, db: Session = Depends(get_db)):
    deleted_todo = crud.delete_user_todo(user_id=user_id, todo_id=todo_id, db=db)
    if deleted_todo:
        return deleted_todo 
    else:
        raise HTTPException(status_code=404, detail="User todo not found")


#NO TOKENS NEEDED
############################################################################################################################################

#REGISTER
#only register a user that has a unique username 
@app.post("/users/", response_model={}, tags=["Register"])
def create_user(user:schemas.UserCreate,db:Session=Depends(get_db)):
    #check if the user already exists 
    created_user = crud.create_user(db=db, user=user) # making sure to hash the password first
    if created_user is None: #user already exists
        raise HTTPException(status_code=404, detail="Username already exists")
    return JWTHandler.signJWT(created_user.username) 
    #TODO return a scheme.User with token and id ?

#LOGIN
@app.post("/auth", response_model={}, tags=["Login"])
def login_user(user:schemas.UserLogin, db:Session=Depends(get_db)):
    if crud.user_exists(user, db):
        return JWTHandler.signJWT(user.username) #if the user exists, create a Token and return it   
    raise HTTPException(status_code=401, detail="Invalid login details!")
    #TODO return a scheme.User with token and id ?


#New secure queries for, so that you cannot post to other accounts  
############################################################################################################################################

#READ USER
@app.get("/user/", dependencies=[Depends(JWTBearer())], response_model=schemas.User, tags=["new"])
def read_user(token:str, db:Session=Depends(get_db)):
    user_id=crud.get_id_from_token(token=token,db=db)
    db_user=crud.get_user_by_id(user_id=user_id,db=db)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

#CREATE ToDo FOR USER
@app.post("/user/todo", dependencies=[Depends(JWTBearer())],response_model=schemas.Todo, tags=["new"])
def add_todo_to_user(todo:schemas.TodoCreate ,token:schemas.Token, db:Session=Depends(get_db)):
    user_id = crud.get_id_from_token(token=token.token, db=db)
    new_todo = crud.create_user_todo_by_id(todo=todo,user_id=user_id, db=db)
    if new_todo:
        return new_todo
    else:
        raise HTTPException(status_code=404, detail="something went wrong, no new todo created")
    
#DELETE A ToDo FROM USER
#TODO what if token is wrong? ->dont get here, because the bearer validated!
@app.delete("/user/todo", dependencies=[Depends(JWTBearer())], response_model=schemas.Todo, tags=["new"])
def delete_user_todo(todo_id:int, token:schemas.Token, db: Session = Depends(get_db)):
    user_id = crud.get_id_from_token(token=token.token,db=db)
    deleted_todo = crud.delete_user_todo(user_id=user_id, todo_id=todo_id, db=db)
    if deleted_todo:
        return deleted_todo 
    else:
        raise HTTPException(status_code=404, detail="User todo not found")
 
 #GETS APP ToDos FROM ONE USER
@app.get("/user/todo", dependencies=[Depends(JWTBearer())] , response_model=List[schemas.Todo], tags=["new"])
def read_todos_from_user(token:str, db:Session=Depends(get_db)):
    user_id = crud.get_id_from_token(token=token, db=db)
    return crud.get_user_todos_by_id(user_id=user_id,db=db)