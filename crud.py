#Create, Read, Update, Delete
from sqlalchemy.orm import Session

import models, schemas

#gets all users
def get_users(db:Session):
    return db.query(models.User).all()

#gets the user with the given id
def get_user(user_id: int, db: Session):
    return db.query(models.User).filter(models.User.id == user_id).first()

#creates a user
def create_user(user:schemas.UserCreate, db: Session):
    if db.query(models.User).filter(models.User.username == user.username).first() is None:
        db_user = models.User(username= user.username, user_password=user.user_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    else:
        return None

#gets all todos
def get_todos(db:Session):
    return db.query(models.Todo).all()

#creates a todo and assigns it to a user
def create_user_todo(todo:schemas.TodoCreate, user_id:int ,db: Session):
    db_todo = models.Todo(**todo.dict(), owner_id=user_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

#gets the todo with the given id
def get_todo(todo_id: int, db: Session):
    return db.query(models.Todo).filter(models.Todo.id == todo_id).first()

#gets all todos of a certain user
def get_user_todos(user_id, db: Session):
    db_user = get_user(user_id=user_id, db=db)
    if db_user:
        return db_user.todos
    return None

#checks if the user has the todo and if yes deletes it
def delete_user_todo(user_id:int, todo_id:int, db:Session):
    user_todos = get_user_todos(user_id=user_id,db=db)
    for todo in user_todos:
        if todo.id == todo_id:
            db.query(models.Todo).filter(models.Todo.id == todo_id).delete()
            db.commit()
            return todo
    return None


def user_exists(user:schemas.UserCreate, db:Session):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if user:
        if db_user.user_password == user.user_password:
            return True
    return False