from app.database import async_session_maker
from sqlalchemy import delete, func, insert, select, update, or_

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
            async with async_session_maker() as session:
                query = insert(cls.model).values(**data)
                result = await session.execute(query)
                await session.commit()
                return result.inserted_primary_key[0] if result.inserted_primary_key else None
            

    @classmethod
    async def update(cls, post_id: int, **data):
        async with async_session_maker() as session:
            query = update(cls.model).where(cls.model.id == post_id).values(**data)
            result = await session.execute(query)
            await session.commit()
            return result.rowcount > 0

        
    @classmethod
    async def delete(cls, post_id: int):
        async with  async_session_maker() as session:
            query = delete(cls.model).where(cls.model.id == post_id)
            result = await session.execute(query)
            await session.commit()
            return result.rowcount > 0

    @classmethod
    async def search_posts(cls, query: str):
        async with async_session_maker() as session:
            statement = select(cls.model).filter(
                or_ (
                    cls.model.title.ilike(f"%{query}%"),
                    cls.model.content.ilike(f"%{query}%")
                )
            )
            result = await session.execute(statement)
            return result.scalars().all()
        
    @classmethod
    async def get_average_posts_per_month(cls, user_id: int):
        async with  async_session_maker() as session:
            subquery = select(func.count().label("post_count")
                              ).where(cls.model.user_id  == user_id
                                   ).group_by(func.date_trunc('month', cls.model.created_at))
            query = select(func.avg(subquery.c.post_count)). select_from(subquery)
            result = await session.execute(query)                                                            
            return result.scalar()
            