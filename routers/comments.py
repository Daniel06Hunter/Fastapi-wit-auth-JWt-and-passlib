from fastapi import APIRouter, Depends, HTTPException 
from pydantic import BaseModel 
from models import Comment,  Post 
from sqlalchemy.orm import Session 
from database import get_db 



router = APIRouter(prefix="/comments", tags=["comments"])

class CreateComment(BaseModel): 
    
    text:str 
    post_id:int 
    
    
@router.post("/") 
async def create_comment(comment_data:CreateComment, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == comment_data.post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    new_comment = Comment(text = comment_data.text, post_id = comment_data.post_id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

@router.get("/") 
async def get_comments(db: Session = Depends(get_db)): 
    return db.query(Comment).all()
     
    
