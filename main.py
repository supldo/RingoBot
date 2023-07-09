from aiogram.utils import executor
from config import dp
from handlers import start
from database import sql_commands

start.register_handlers_start(dp=dp)


async def on_startup(_):
    db = sql_commands.Database()
    db.sql_create_db()
    print("Bot is ready!")


if __name__ == "__main__":
    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=on_startup
                           )
