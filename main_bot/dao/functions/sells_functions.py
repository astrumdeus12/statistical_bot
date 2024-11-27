from ..settings import get_async_session
from ..models.main_models import Sells, User
from sqlalchemy import select, update, func
from sqlalchemy.orm import selectinload
from datetime import date, timedelta

async def create_user_sells_or_update(tg_id: str, argument_name, amount):
    async for session in get_async_session():
        async with session.begin():
            
            day = date.today()
            user_sells = await session.execute(select(Sells).where(Sells.user_id == tg_id).where(Sells.day == day))
        
            result = user_sells.scalars().first()
        
            if result is None:
                session.add(Sells(user_id = tg_id, day = day, **{argument_name:amount}))
            
            else:
                current_amount = getattr(result, argument_name, 0)  
                new_amount = current_amount + amount  
                await session.execute(update(Sells).where(Sells.id == result.id).values(**{argument_name: new_amount}))
            
            await session.commit()
        
        
        
        
async def get_user_sells_statistic(days:int, user_tg_id:str):
    async for session in get_async_session():
        async with session.begin():
            time_delta = date.today() - timedelta(days=days)
            user_sells = await session.execute(
                select(
                    Sells.user_id,
                    User.name.label('user_name'),  # Изменено на User.name
                    func.sum(Sells.credits).label('total_credits'),
                    func.sum(Sells.insurance).label('total_insurance'),
                    func.sum(Sells.client_calls).label('total_client_calls'),
                    func.sum(Sells.deb_cards).label('total_deb_cards'),
                    func.sum(Sells.credit_cards).label('total_credit_cards'),
                    func.sum(Sells.investition_insurance).label('total_investition_insurance')
                ).join(User)  # Объединяем с таблицей пользователей
                .where(Sells.user_id == user_tg_id)  # Фильтруем по конкретному пользователю
                .where(Sells.day > time_delta)
                .group_by(Sells.user_id, User.name)  # Группируем по ID и имени пользователя
            )
            result = user_sells.fetchone()  # Получаем первую (и единственную) строку результата

            # Формируем ответ
            if result:
                result_answer = f'''\n Имя: {result.user_name} \n Кредиты: {result.total_credits or 0} \n Страховки: {result.total_insurance or 0} \n Звонки: {result.total_client_calls or 0} \n Дебетовые карты: {result.total_deb_cards or 0} \n Кредитные карты: {result.total_credit_cards or 0} \n Инвестиционное страхование жизни: {result.total_investition_insurance or 0}'''
            else:
                result_answer = 'Нет данных за указанный период.'
            await session.commit()
            return result_answer
        
        
        
        
async def get_all_sells_statistic(days:int):
    async for session in get_async_session():
        async with session.begin():
            time_delta = date.today() - timedelta(days=days)
            user_sells = await session.execute(
                select(
                    Sells.user_id,
                    User.name.label('user_name'),  # Получаем имя пользователя
                    func.sum(Sells.credits).label('total_credits'),
                    func.sum(Sells.insurance).label('total_insurance'),
                    func.sum(Sells.client_calls).label('total_client_calls'),
                    func.sum(Sells.deb_cards).label('total_deb_cards'),
                    func.sum(Sells.credit_cards).label('total_credit_cards'),
                    func.sum(Sells.investition_insurance).label('total_investition_insurance')
                ).join(User)  # Объединяем с таблицей пользователей
                .where(Sells.day > time_delta)  # Фильтруем по дате
                .group_by(Sells.user_id, User.name)  # Группируем по ID и имени пользователя
            )
            results = user_sells.fetchall()  # Получаем все результаты

            # Формируем ответ
            result_answer = ''
            for result in results:
                result_answer += f'''\n Имя: {result.user_name} \n Кредиты: {result.total_credits or 0} \n Страховки: {result.total_insurance or 0} \n Звонки: {result.total_client_calls or 0} \n Дебетовые карты: {result.total_deb_cards or 0} \n Кредитные карты: {result.total_credit_cards or 0} \n Инвестиционное страхование жизни: {result.total_investition_insurance or 0} \n'''
            
            if not result_answer:
                result_answer = 'Нет данных за указанный период.'

            await session.commit()
            return result_answer