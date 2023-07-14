from config import bot
from aiogram import types

async def user_id(message: types.Message):
    await bot.send_message(message.chat.id, f'Ваш ID: {message.from_user.id}')