from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

async def create_admin_keyboard(user_id):
    return InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = 'Да', callback_data=f'yes_{user_id}'),InlineKeyboardButton(text = 'Нет', callback_data=f'no_{user_id}')]])