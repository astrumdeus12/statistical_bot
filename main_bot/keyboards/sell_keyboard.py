from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

sell_type_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [ 
     InlineKeyboardButton(text='Кредитные карты', callback_data='credit_cards'),
     InlineKeyboardButton(text='Дебетовые карты', callback_data='deb_cards')],
    
    [InlineKeyboardButton(text='Кредиты', callback_data='credits'),
     InlineKeyboardButton(text='Страховки', callback_data='insurance'),
     InlineKeyboardButton(text='Звонки', callback_data='client_calls')],
    [InlineKeyboardButton(text='Инвестиционное страхование жизни', callback_data='investition_insurance')],
    ])