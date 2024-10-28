from fastapi import APIRouter
from app.excecptions import ErrorAdding, PageNotFound
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
        raise PageNotFound
    return post

@router.post("/", response_model=Post)
async def create_post(post: PostCreate):
    post_id =  await PostDAO.add(**post.dict())
    if post_id is None:    
        raise ErrorAdding
    created_post = await PostDAO.find_by_id(post_id)
    if created_post is None:
        raise PageNotFound
    return created_post
        

@router.put("/{post_id}", response_model=Post)
async def update_post(post_id: int, post: PostUpdate):
    updated = await PostDAO.update(post_id, **post.dict(exclude_unset=True))
    if not updated:
        raise PageNotFound
    return await PostDAO.find_by_id(post_id)

@router.delete("/{post_id}")
async def delete_post(post_id: int):
    deleted = await PostDAO.delete(post_id)
    if not deleted:
        raise PageNotFound
    return {"detail": "Пост удален"}
