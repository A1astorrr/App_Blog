from app.database import async_session_maker
from sqlalchemy import insert, select

class BaseDAO:
    model = None
    
    @classmethod
    async def find_all(cls, skip: int = 0, limit: int = 100):
        async with async_session_maker() as session:
            query = select(cls.model).offset(skip).limit(limit)
            result = await session.execute(query)
            return result.scalars().all()
        
    @classmethod
    async def find_by_id(cls, post_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=post_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()
        
    @classmethod
    async def add(cls,  **data):
        async with  async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()