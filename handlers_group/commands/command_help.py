from config import bot
from aiogram import types
from handlers_group.const import HELP_TEXT

async def help_button(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=HELP_TEXT)