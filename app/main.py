from fastapi import FastAPI
from app.posts.router import router as router_posts

app = FastAPI()
app.include_router(router_posts)
