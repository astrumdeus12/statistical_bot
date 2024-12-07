from ..settings import get_async_session
from ..models.main_models import User


async def create_user(username: str, phone_number: str, tg_id:str):
    async for session in get_async_session():
        async with session.begin():
            new_user = User(name = username, phone_number = phone_number, tg_id = tg_id)
            session.add(new_user)
            await session.commit()
        
