#structure of the db-elements
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Todo(Base):
    __tablename__ = "todos"
    
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    dueTo = Column(DateTime, nullable=False)
    completed = Column(Boolean, nullable=False)
    description = Column(String, nullable=True)
    importance = Column(Integer, nullable=False)
    user_ip  = Column(Integer, ForeignKey('user.id'), nullable=True) #forein key of the user (the int equals the id of the user)
    
    # def __repr__(self) -> str:
    #     return f"Todo(id={self.id}, name={self.name}, dueTo={self.dueTo}, completed={self.completed}, description={self.description}, importance={self.importance})"

class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True,index=True)
    username = Column(String, nullable=False)
    user_email=Column(String, nullable=False)
    user_password = Column(Integer, nullable=False)
    todos = relationship("Todo", backref="user") #putting a new column on the todo -> a user column
#     #add more information later?!