from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from  ..keyboards.statistic_keyboards import select_type_statistic, select_period
from pydantic import  BaseModel, ValidationError
from ..dao.functions.sells_functions import get_user_sells_statistic, get_all_sells_statistic
from sqlalchemy.exc import IntegrityError


statistic_router = Router()
type_list = ['self', 'all']
period_list = ['1', '7', '30']
class Statistic(StatesGroup):
    noun = State()
    period = State()

@statistic_router.message(Command('statistic'))
async def start_statistic(message: Message):
    await message.reply('Выберите чьи результаты хотите увидеть:', reply_markup=select_type_statistic)
    
    
@statistic_router.callback_query(F.data.in_(type_list))
async def select_period_statistic(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.update_data(noun = callback.data)
    await state.set_state(Statistic.period)
    await callback.message.reply('Выберите период продаж:', reply_markup=select_period)

@statistic_router.callback_query(F.data.in_(period_list))
async def get_statistic(callback: CallbackQuery, state: FSMContext):
    await state.update_data(period = callback.data)
    data = await state.get_data()
    await state.clear()
    result = ''
    if data['noun'] == 'self':
        result = await get_user_sells_statistic(int(data['period']), user_tg_id= str(callback.from_user.id))
    else:
        result = await get_all_sells_statistic(int(data['period']))
    await callback.message.answer(result)