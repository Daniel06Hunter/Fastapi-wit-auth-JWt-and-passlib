from fastapi import APIRouter, Depends, HTTPException 
from pydantic import BaseModel 
from sqlalchemy.orm import Session 

from database import get_db 
from models import Post, User 
from security import get_current_user  # Импортируем проверку пользователя

router = APIRouter(prefix="/posts", tags=["posts"])

# Больше нет поля owner_id! Клиент шлет только title и content
class PostCreate(BaseModel): 
    title: str
    content: str 
    
@router.post("/")
async def create_post(
    post_data: PostCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # <--- Магия авторизации!
): 
    # Создаем пост и автоматически привязываем к ID текущего вошедшего юзера
    new_post = Post(
        title=post_data.title, 
        content=post_data.content, 
        owner_id=current_user.id  # Берем из токена
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
    
@router.get("/")
async def get_posts(db: Session = Depends(get_db)): 
    return db.query(Post).all()