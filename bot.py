import asyncio
import logging
from main_bot.handlers.main_handlers import registrate_router
from main_bot.handlers.sell_handlers import sell_router
from main_bot.handlers.statistic_handlers import statistic_router
from config import bot, dp






async def main() -> None:
    
    

    dp.include_router(registrate_router)
    dp.include_router(sell_router)
    dp.include_router(statistic_router)
    
    await dp.start_polling(bot)
    


    
logging.basicConfig(level=logging.INFO)
asyncio.run(main())
