from database import Base 
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

class User(Base): 
    __tablename__ = "users"
    
    id = Column(Integer, primary_key = True, index=True)
    
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable = False)
    hashed_password = Column(String, nullable=False)
    
    
    # Связь: один пользователь -> много постов
    posts = relationship("Post", back_populates="owner")



class Post(Base): 
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key = True, index = True)
    title = Column(String, nullable = False) 
    content = Column(String, nullable = False) 
    
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    # Связи:
    owner = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete")
    

class Comment(Base): 
    __tablename__ = "comments"
    
    id=Column(Integer, primary_key=True, index=True) 
    text = Column(String,  nullable = False) 
    post_id = Column(Integer, ForeignKey("posts.id"))
    
    # Связь: комментарий принадлежит одному посту
    post = relationship("Post", back_populates="comments")
    
    
    