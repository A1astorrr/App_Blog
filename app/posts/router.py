from fastapi import APIRouter
from app.posts.dao import PostDAO
from app.posts.schemas import Post

router = APIRouter(
    prefix="/posts",
    tags=["Посты"],
)

@router.get('/', response_model=list[Post])
async def read_posts(skip: int = 0, limit: int = 100):
    return await PostDAO.find_all(skip=skip, limit=limit)