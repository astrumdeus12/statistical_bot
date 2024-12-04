from ..settings import get_async_session
from ..models.main_models import Sells
from sqlalchemy import select, update
from datetime import date

async def create_user_sells_or_update(tg_id: str, argument_name, amount, count):
    async for session in get_async_session():
        async with session.begin():
            
            day = date.today()
            user_sells = await session.execute(select(Sells).where(Sells.user_id == tg_id).where(Sells.day == day))
        
            result = user_sells.scalars().first()
        
            if result is None:
                session.add(Sells(user_id = tg_id, day = day, **{argument_name:amount}))
            
            else:
                current_amount = getattr(result, argument_name, 0)  

                current_count = getattr(result, 'credit_count', 0) 
                count += current_count
                new_amount = current_amount + amount  
                await session.execute(update(Sells).where(Sells.id == result.id).values(**{argument_name: new_amount}).values(credit_count = count))
            
            await session.commit()
        
        
        
        
