from fastapi import FastAPI, Path, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import List
import datetime
import json

import models, schemas, crud
from database import engine, SessionLocal 

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


######################################################################################################################################################


@app.get("/todos/", response_model=List[schemas.Todo])
def read_todos(db:Session=Depends(get_db)):
    return crud.get_todos(db)

@app.post("/users/", response_model=schemas.User)
def create_user(user:schemas.UserCreate,db:Session=Depends(get_db)):
    #check if the user already exists 
    return crud.create_user(db=db, user=user)

@app.get("/users", response_model=List[schemas.User])
def read_users(db:Session=Depends(get_db)):
    users=crud.get_users(db)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db:Session=Depends(get_db)):
    db_user=crud.get_user(user_id=user_id,db=db)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/todo/", response_model=schemas.Todo)
def create_todo_for_user(user_id:int, todo:schemas.TodoCreate, db:Session=Depends(get_db)):
    return crud.create_user_todo(todo=todo, user_id=user_id, db=db)


######################################################################################################################################################


# @app.put("/todo")
# def replace_todo(todo_id: int, todo:schemas.Todo, db: Session = Depends(get_db)):
#     todo_model = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    
#     if todo_model is None: 
#         raise HTTPException(
#             status_code=404,
#             detail=f"ID {todo_id} : Does not exist"
#         )
#     #update the books values
#     todo_model.name = todo.name
#     todo_model.dueTo = todo.dueTo
#     todo_model.completed = todo.completed
#     todo_model.description = todo.description
#     todo_model.importance = todo.importance
    
#     todo_model.user_id = todo.user_id
    
#     db.add(todo_model)
#     db.commit()
    
#     return todo
       
# @app.delete("/todo")
# def delete_todo(todo_id: int, db: Session = Depends(get_db)):
#     todo_model = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
#     #check if the todo exists
#     if todo_model is None:
#         raise HTTPException(
#             status_code=404,
#             detail=f"ID {todo_id} does not exist"
#         )
#     #if it does exist delete all todos with the handed id
#     db.query(models.Todo).filter(models.Todo.id == todo_id).delete()
#     db.commit()
#     return json.loads('{"deleted": true}')