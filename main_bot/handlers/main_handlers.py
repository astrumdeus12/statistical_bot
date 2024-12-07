from aiogram import Router, F
from aiogram.filters import Command, CommandStart, or_f
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from ..dao.functions.user_functions import create_user
from ..keyboards.admin_keyboards import  create_admin_keyboard
from config import bot, ADMIN_ID

registrate_router = Router()

class Registrator(StatesGroup):
    name = State()
    number = State()
    new_user_id = State()
    
    
        

users_to_auth = []


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
    if message.text.isalpha():
        await state.update_data(name = message.text)
        await state.set_state(Registrator.number)
        await message.answer('Введите номер телефона (без +7)')
    else:
        await state.set_state(Registrator.name)
        await message.answer('Имя содержит недопустимые символы. \n Введите имя заново:')
    
    
@registrate_router.message(Registrator.number)
async def registrate_admin_access(message: Message, state: FSMContext):
    if message.text.isdigit() and len(message.text) == 10:
        await state.update_data(number = message.text, new_user_id = str(message.from_user.id))
        data = await state.get_data()
        print(data)
        users_to_auth.append(data)
        await bot.send_message(chat_id=ADMIN_ID, 
                            text=f'Запрос на регистрацию от пользователя: \n {data['name']} \n {data['number']} \n id: {data['new_user_id']} \n Разрешить доступ?', 
                            reply_markup= await create_admin_keyboard(str(message.from_user.id))
                            )
        await state.clear()
        await message.answer('Ожидайте разрешение администратора.')
        
    else:
        await state.set_state(Registrator.number)
        await message.answer('Вы ввели неккоректный номер телефона. \n Введите номер телефона заново (без +7):')
        


@registrate_router.callback_query(or_f(F.data.startswith('yes_'), F.data.startswith('no_')))
async def end_registrate(callback: CallbackQuery, state: FSMContext):
    
    action, user_id = callback.data.split('_')
    new_user = [user for user in users_to_auth if user['new_user_id'] == user_id][0]
    users_to_auth.remove(new_user)
    
    
    await bot.delete_message(chat_id=callback.message.chat.id,
                                 message_id=callback.message.message_id)
    
    if action == 'yes':
        await create_user(new_user['name'], new_user['number'], new_user['new_user_id'])
        await callback.message.answer(text='Доступ пользователю разрешен.')
        await bot.send_message(chat_id=new_user['new_user_id'],
                               text='Регистрация завершена. Доступ разрешен')
        
        
    else:
        await callback.message.answer(text='Доступ пользователю запрещен.')
        await bot.send_message(chat_id=new_user['new_user_id'],
                               text='Доступ запрещен.')
        
    await state.clear()
    

    
    