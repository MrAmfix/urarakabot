import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from router import urt


bot = Bot(token=BOT_TOKEN)


async def main():
    print('Bot started')
    dp = Dispatcher()
    dp.include_routers(urt)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    asyncio.run(main())
