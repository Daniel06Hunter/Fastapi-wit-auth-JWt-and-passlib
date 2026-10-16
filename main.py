from fastapi import FastAPI 
from database import engine, Base
from routers import users, posts, comments, auth

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(auth.router)




@app.get("/")
async def root():
    return {"message": "Hello Russia/ Go to /docs/ for more information"}
    