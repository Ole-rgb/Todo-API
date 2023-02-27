#structure of the db-elements
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True,index=True)
    username = Column(String,unique=True, nullable=False)
    # user_email=Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    todos = relationship("Todo", back_populates="owner")
    
class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    dueTo = Column(DateTime, nullable=False)
    completed = Column(Boolean, nullable=False)
    description = Column(String, nullable=True)
    importance = Column(Integer, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    owner  = relationship("User", back_populates="todos")