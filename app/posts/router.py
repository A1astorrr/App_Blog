from fastapi import APIRouter
from app.exceptions import PostNotFound
from app.posts.dao import PostDAO
from app.posts.schemas import Post, PostCreate, PostUpdate

router = APIRouter(
    prefix="/posts",
    tags=["Посты"],
)

@router.get('/', response_model=list[Post])
async def read_posts(skip: int = 0, limit: int = 100):
    return await PostDAO.find_all(skip=skip, limit=limit)

@router.get("/{post_id}", response_model=Post)
async def read_post_by_id(post_id: int):
    post =  await PostDAO.find_by_id(post_id)
    if post is None:
        raise PostNotFound
    return post

@router.post("/", response_model=Post)
async def create_post(post: PostCreate):
    return await PostDAO.add(**post.dict())

@router.put("/{post_id}", response_model=Post)
async def update_post(post_id: int, post: PostUpdate):
    updated = await PostDAO.update(post_id, **post.dict(exclude_unset=True))
    if not updated:
        raise PostNotFound
    return updated

@router.delete("/{post_id}", response_model=Post)
async def delete_post(post_id: int):
    deleted = await PostDAO.delete(post_id)
    if not deleted:
        raise PostNotFound
    return {"detail": "Пост удален"}


# @router.get("/search")

# @router.get("/statistics/{user_id}")
