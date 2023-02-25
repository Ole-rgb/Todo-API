#structure of the db-elements
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from database import Base

class Todos(Base):
    __tablename__ = "todos"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    dueTo = Column(DateTime, nullable=False)
    completed = Column(Boolean, nullable=False)
    description = Column(String, nullable=True)
    importance = Column(Integer, nullable=False)
    
    def __repr__(self) -> str:
        return f"Todo(id={self.id}, name={self.name}, dueTo={self.dueTo}, completed={self.completed}, description={self.description}, importance={self.importance})"


class User(Base):
    __tablename__ = "user_account"
    
    user_id = Column(Integer, primary_key=True,index=True)
    username = Column(String, nullable=True)
    user_email=Column(String, nullable=False)
    user_password = Column(Integer, nullable=False)
    #add more information later?!