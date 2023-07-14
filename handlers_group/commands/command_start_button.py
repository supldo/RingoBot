from aiogram import types
from database.sql_commands import Database
from keyboards import start_keyboard

async def start_button(message: types.Message):
    id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    Database().sql_insert_user(id=id,
                               username=username,
                               first_name=first_name,
                               last_name=last_name)
    await message.reply(text=f"Привет {message.from_user.first_name}!",
                        reply_markup=start_keyboard.start_markup)