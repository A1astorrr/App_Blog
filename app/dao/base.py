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