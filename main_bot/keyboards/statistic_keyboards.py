from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

select_type_statistic = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = 'Личная', callback_data='self'),InlineKeyboardButton(text = 'Общая', callback_data='all')]
])

select_period = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = 'Сегодня', callback_data='1'),InlineKeyboardButton(text = 'Неделя', callback_data='7'), InlineKeyboardButton(text = 'Месяц', callback_data='30')]
])