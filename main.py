from aiogram.utils import executor
from config import dp
from handlers_admin import admin
from handlers_group import commands, async_ongoing
from database import sql_commands


admin.register_handler_admin(dp=dp)
async_ongoing.register_scrapers_ongoing(dp=dp)
commands.register_handlers(dp=dp)

PROXY_URL = "https://proxy.server:3128"

async def on_startup(_):
    db = sql_commands.Database()
    db.sql_create_db()
    print("Бот запущен!")


if __name__ == "__main__":
    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=on_startup
                           )
