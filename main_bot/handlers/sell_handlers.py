from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from  ..keyboards.sell_keyboard import sell_type_keyboard
from pydantic import  BaseModel, ValidationError
from ..dao.functions.sells_functions import create_user_sells_or_update
from sqlalchemy.exc import IntegrityError

sell_router = Router()

sell_list = ['credits', 'insurance', 'box_insurance', 'investition_insurance', 'credit_cards', 'deb_cards', 'client_calls']

class SellerData(BaseModel):
    type_sell : str
    number : int
    count : int

class Seller(StatesGroup):
    type_sell : str = State()
    number : int = State()
    count : int = State()
    
    
@sell_router.message(Command('make_sell'))
async def select_type_of_sell(message: Message):
    await message.reply('Выберите тип продажи:', reply_markup=sell_type_keyboard)
    
    
@sell_router.callback_query(F.data.in_(sell_list[1:]))
async def get_count_of_sell(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.update_data(type_sell = callback.data)
    await state.update_data(count = 0)
    await state.set_state(Seller.number)
    sum_or_count = 'сумму' if sell_list.index(callback.data) <= 3 else 'количество'
    await callback.message.answer(f'Введите {sum_or_count} продаж:')



@sell_router.callback_query(F.data == 'credits')
async def get_credits_count(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.update_data(type_sell = callback.data)
    await state.set_state(Seller.count)
    
    await callback.message.answer('Введите количество кредитов:')
    
    
    
    
@sell_router.message(Seller.count)
async def get_summ_of_credits(message: Message, state: FSMContext):
    
    await state.update_data(count = message.text)
    await state.set_state(Seller.number)
    await message.answer('Введите сумму продаж:')



@sell_router.message(Seller.number)
async def make_sell(message: Message, state: FSMContext):
    try:
        await state.update_data(number = message.text)
        data = await state.get_data()
        validate_data = SellerData(**data)
        
        await create_user_sells_or_update(str(message.from_user.id), validate_data.type_sell, int(validate_data.number), validate_data.count)
        
        await state.clear()
        await message.answer('Вы добавили продажу. \nСоверишть новую продажу: /make_sell или выберите тип продажи выше.')
    except ValidationError:
        await message.answer('Вы ввели неверный тип данных, начните оформление продажи занова нажав /make_sell')
    except IntegrityError:
        await message.answer('Для совершения продаж зарегистрируйтесь: /registrate')