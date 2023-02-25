from fastapi import FastAPI, Path, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
import datetime
import json

import models
from database import engine, SessionLocal 


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



#creates the db-table
models.Base.metadata.create_all(bind=engine)

#handles sessions
def get_db():
   db = SessionLocal()
   try:
       yield db
   finally:
       db.close()

#models at todo db-element (no id needed)
class Todos(BaseModel):
    name: str = Field(min_length=1)
    dueTo: datetime
    completed: bool
    description: str = Field(max_length=100)
    importance: int = Field(gt=-1, lt=6)


@app.get("/")
def get_todos(db: Session = Depends(get_db)):
    return db.query(models.Todos).all()

@app.post("/")
def create_todo(todo: Todos, db: Session = Depends(get_db)):
    #create a todo model and fill it with the information from todo
    todo_model = models.Todos()
    todo_model.name = todo.name
    todo_model.dueTo = todo.dueTo
    todo_model.completed = todo.completed
    todo_model.description = todo.description
    todo_model.importance = todo.importance
    
    #add todomodel to db
    db.add(todo_model)
    db.commit()
    return todo


@app.put("/")
def replace_todo(todo_id: int, todo:Todos, db: Session = Depends(get_db)):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    
    if todo_model is None: 
        raise HTTPException(
            status_code=404,
            detail=f"ID {todo_id} : Does not exist"
        )
        
    #update the books values
    todo_model.name = todo.name
    todo_model.dueTo = todo.dueTo
    todo_model.completed = todo.completed
    todo_model.description = todo.description
    todo_model.importance = todo.importance
    
    db.add(todo_model)
    db.commit()
    
    return todo
    
        
@app.delete("/")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    #check if the todo exists
    if todo_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {todo_id} does not exist"
        )
    #if it does exist delete all todos with the handed id
    db.query(models.Todos).filter(models.Todos.id == todo_id).delete()
    db.commit()
    return json.loads('{"deleted": true}')
    
    


