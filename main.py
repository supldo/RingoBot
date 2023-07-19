from aiogram.utils import executor
from config import dp
from handlers_admin import admin
from handlers_group import commands
from database import sql_commands

admin.register_handler_admin(dp=dp)
commands.register_handlers(dp=dp)

async def on_startup(_):
    db = sql_commands.Database()
    db.sql_create_db()
    print("Бот запущен!")


if __name__ == "__main__":
    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=on_startup
                           )
