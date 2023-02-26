#Create, Read, Update, Delete
from sqlalchemy.orm import Session
import models, schemas

def get_users(db:Session):
    return db.query(models.User).all()

def get_user(user_id: int, db: Session):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(user:schemas.UserCreate, db: Session):
    db_user = models.User(username= user.username, user_email=user.user_email, user_password=user.user_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_todos(db:Session):
    return db.query(models.Todo).all()

def create_user_todo(todo:schemas.TodoCreate, user_id:int ,db: Session):
    db_todo = models.Todo(**todo.dict(), owner_id=user_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo