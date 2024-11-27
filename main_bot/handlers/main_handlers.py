from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from ..dao.functions.user_functions import create_user


registrate_router = Router()

class Registrator(StatesGroup):
    name = State()
    number = State()
    secret_code = State()


@registrate_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Добрый день \n Для начала зарегистрируйтесь: /registrate \n Доступные команды после регистрации:\n /make_sell - сделать продажу \n /statistic - посмотреть статистику продаж')
    
    
    
@registrate_router.message(Command('registrate'))
async def start_registrate(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(Registrator.name)
    await message.answer('Введите ваше имя:')

@registrate_router.message(Registrator.name)
async def registrate_number(message: Message, state: FSMContext):
    await state.update_data(name = message.text)
    await state.set_state(Registrator.number)
    await message.answer('Введите номер телефона (без +7)')
    
@registrate_router.message(Registrator.number)
async def registrate_secret_code(message: Message, state: FSMContext):
    await state.update_data(number = message.text)
    await state.set_state(Registrator.secret_code)
    await message.answer('Введите код: ')

@registrate_router.message(Registrator.secret_code)
async def end_registrate(message: Message, state: FSMContext):
    await state.update_data(secret_code = message.text)
    data = await state.get_data()
    await create_user(data['name'], data['number'], str(message.from_user.id))
    await state.clear()
    await message.answer(f'Регистрация завершена, ваше имя: {data['name']}, ваш номер телефона: {'+7' + data['number']}')    