import logging
import asyncio
from aiogram import Bot, Dispatcher
from config import bot, dp, TOKEN
# from app.handlers import router
from handlers import router

async def main():
    
    dp.include_router(router)
    logging.info("Routers included. Starting polling...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

