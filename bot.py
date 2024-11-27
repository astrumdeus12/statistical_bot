import asyncio
import logging
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher

from main_bot.handlers.main_handlers import registrate_router
from main_bot.handlers.sell_handlers import sell_router
from main_bot.handlers.statistic_handlers import statistic_router
from config import TOKEN_BOT

bot = Bot(token=TOKEN_BOT, default=DefaultBotProperties(parse_mode=ParseMode.HTML))





async def main() -> None:
    try:
        dp = Dispatcher()

        dp.include_router(registrate_router)
        dp.include_router(sell_router)
        dp.include_router(statistic_router)

        await dp.start_polling(bot)
    except KeyboardInterrupt:
        print('Exit')

    
logging.basicConfig(level=logging.INFO)
asyncio.run(main())
