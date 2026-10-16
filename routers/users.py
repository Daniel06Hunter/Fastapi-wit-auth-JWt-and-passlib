from fastapi import APIRouter, Depends, HTTPException 
from pydantic import BaseModel, EmailStr 
from database import SessionLocal, get_db 
from models import User
from sqlalchemy.orm import Session 
from security import hash_password

router = APIRouter(prefix="/users", tags=["Users"])

class UserCreate(BaseModel): 
    username : str 
    password:str
    email:str 
    
    
@router.post("/") 
async def create_user(user_data:UserCreate, db: Session = Depends(get_db) ):
    existing_user = db.query(User).filter((User.email == user_data.email) | (User.username == user_data.username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    
    new_user = User(username=user_data.username, email=user_data.email, hashed_password=hash_password(user_data.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user) 
    return(new_user)

@router.get("/") 
async def get_users(db: Session = Depends(get_db)): 
    return db.query(User).all()




