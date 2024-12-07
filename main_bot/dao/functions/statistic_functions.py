from ..settings import get_async_session
from ..models.main_models import Sells, User
from sqlalchemy import  select, func
from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP


async def count_premium(result : dict):
    credit_cards_prem = Decimal(result['total_credit_cards']) * Decimal(250)
    box_insurance_prem = Decimal(result['box_insurance']) * Decimal(5/100)
    investition_insurance_prem = Decimal(result['total_investition_insurance']) * Decimal(15/1000)
    deb_cards_prem = Decimal(result['total_deb_cards']) * Decimal(150)
    credits_prem = Decimal(result['total_credits']) * Decimal((7/10000 if result['total_credit_count'] < 6 else 18/10000)) + Decimal(( min([result['total_credit_count'] - 8, result['period_credit_count']]) *300 ) if result['total_credit_count'] >8 else 0)
    credit_insurance_prem = Decimal(result['total_insurance']) * Decimal(11/1000)
    total_prem = Decimal(credit_cards_prem) + Decimal(box_insurance_prem) + Decimal(investition_insurance_prem) + Decimal(deb_cards_prem) + Decimal(credits_prem) + Decimal(credit_insurance_prem)
    return total_prem.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
    



async def get_user_sells_statistic(days:int, user_tg_id:str):
    async for session in get_async_session():
        async with session.begin():
            time_delta = date.today() - timedelta(days=days)
            first_day_current_month = date.today().replace(day=1)
            last_day_current_month = (first_day_current_month + timedelta(days=31)).replace(day=1) - timedelta(days=1)
            user_sells = await session.execute(
                select(
                    Sells.user_id.label('user_tg_id'),
                    User.name.label('user_name'), 
                    func.sum(Sells.credits).label('total_credits'),
                    func.sum(Sells.insurance).label('total_insurance'),
                    func.sum(Sells.client_calls).label('total_client_calls'),
                    func.sum(Sells.deb_cards).label('total_deb_cards'),
                    func.sum(Sells.credit_cards).label('total_credit_cards'),
                    func.sum(Sells.investition_insurance).label('total_investition_insurance'),
                    func.sum(Sells.box_insurance).label('box_insurance'),
                    func.sum(Sells.credit_count).label('period_credit_count'),
                ).join(User)  
                .where(Sells.user_id == user_tg_id)  
                .where(Sells.day > time_delta)
                .group_by(Sells.user_id, User.name)  
            )
            result_period = user_sells.fetchone()  
            
            
            
            user_credits_count_month = await session.execute(
                select(
                    func.sum(Sells.credit_count).label('total_credit_count'),
                ).join(User)  
                .where(Sells.user_id == user_tg_id)  
                .where(Sells.day >= first_day_current_month)
                .where(Sells.day <= last_day_current_month)  
            )
            credits_count = user_credits_count_month.fetchone()
            
            result = {}
            if result_period:
                result.update({k: getattr(result_period, k) for k in result_period._mapping})
                result['total_credit_count'] = credits_count.total_credit_count if credits_count else 0
                print(credits_count, credits_count is None)
                print(result['total_credit_count'])
            else:
                result = {'user_name': 'Нет данных', 'total_credits': 0, 'total_insurance': 0, 'box_insurance': 0, 'total_client_calls':0, 'total_deb_cards': 0, 'total_credit_cards': 0, 'total_investition_insurance': 0, 'period_credit_count': 0, 'total_credit_count': 0}


            if result:
                result_answer = f'''\n Имя: {result['user_name']} \n Кредиты: {result['total_credits'] or 0} \n Страховки: {result['total_insurance'] or 0} \n Коробочные страхования: {result['box_insurance']} \n Звонки: {result["total_client_calls"] or 0} \n Дебетовые карты: {result['total_deb_cards'] or 0} \n Кредитные карты: {result["total_credit_cards"] or 0} \n Инвестиционное страхование жизни: {result["total_investition_insurance"] or 0}'''
                premium = await count_premium(result)
                result_answer += f'\n Полученная премия +{premium} рублей'
            else:
                result_answer = 'Нет данных за указанный период.'
            await session.commit()
            return result_answer
        
        
        
        
        
        
async def get_all_sells_statistic(days:int):
    async for session in get_async_session():
        async with session.begin():
            time_delta = date.today() - timedelta(days=days)
            first_day_current_month = date.today().replace(day=1)
            last_day_current_month = (first_day_current_month + timedelta(days=31)).replace(day=1) - timedelta(days=1)
            user_sells = await session.execute(
                select(
                    Sells.user_id.label('user_tg_id'),
                    User.name.label('user_name'), 
                    func.sum(Sells.credits).label('total_credits'),
                    func.sum(Sells.insurance).label('total_insurance'),
                    func.sum(Sells.client_calls).label('total_client_calls'),
                    func.sum(Sells.deb_cards).label('total_deb_cards'),
                    func.sum(Sells.credit_cards).label('total_credit_cards'),
                    func.sum(Sells.investition_insurance).label('total_investition_insurance'),
                    func.sum(Sells.box_insurance).label('box_insurance'),
                    func.sum(Sells.credit_count).label('period_credit_count'),
                ).join(User)  
                .where(Sells.day > time_delta)
                .group_by(Sells.user_id, User.name))
            
            period_result = user_sells.fetchall()  
            
            
            user_credits_count_month = await session.execute(
                select(
                    Sells.user_id.label('user_tg_id'),
                    func.sum(Sells.credit_count).label('total_credit_count')
                )   
                .where(Sells.day >= first_day_current_month)
                .where(Sells.day <= last_day_current_month)
                .group_by(Sells.user_id))
            
            credits_count = user_credits_count_month.fetchall()
            
            results = []
            print(period_result)
            for user in period_result:
                result = {}
                result.update({k: getattr(user, k) for k in user._mapping})
                result['total_credit_count'] = 0
                for counts in credits_count:
                    print(counts.total_credit_count)
                    if counts.user_tg_id == result['user_tg_id']:
                        result['total_credit_count'] = counts.total_credit_count 
                print(result)
                result['premium'] = await count_premium(result)
                results.append(result)
                
            sorted_users = sorted(results, key = lambda x: x['premium'], reverse=True)
            
            for rank, user in enumerate(sorted_users, start=1):
                user['rank'] = rank
                
                
            result_answer = ''
            second_result_answer = ''
            for result in sorted_users:
                if result['rank'] < 10:
                    result_answer += f'''\n Топ {result['rank']} \n Имя: {result['user_name']} \n Кредиты: {result['total_credits'] or 0} \n Страховки: {result['total_insurance'] or 0} \n Коробочные страхования: {result['box_insurance']} \n Звонки: {result["total_client_calls"] or 0} \n Дебетовые карты: {result['total_deb_cards'] or 0} \n Кредитные карты: {result["total_credit_cards"] or 0} \n Инвестиционное страхование жизни: {result["total_investition_insurance"] or 0}'''
                    result_answer += f'\n Полученная премия +{result['premium']} рублей \n'
                else:
                    second_result_answer += f'''\n Топ {result['rank']} \n Имя: {result['user_name']} \n Кредиты: {result['total_credits'] or 0} \n Страховки: {result['total_insurance'] or 0} \n Коробочные страхования: {result['box_insurance']} \n Звонки: {result["total_client_calls"] or 0} \n Дебетовые карты: {result['total_deb_cards'] or 0} \n Кредитные карты: {result["total_credit_cards"] or 0} \n Инвестиционное страхование жизни: {result["total_investition_insurance"] or 0}'''
                    second_result_answer += f'\n Полученная премия +{result['premium']} рублей \n'
            total_answer = [] 
            if not result_answer:
                result_answer = 'Нет данных за указанный период.'
            if second_result_answer:
                total_answer.append(second_result_answer)
            total_answer.append(result_answer)

            await session.commit()
            return total_answer