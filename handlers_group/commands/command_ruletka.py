from config import bot
from aiogram import types
from random import randint
from datetime import datetime, timedelta

revolver = [False] * 6
revolver[randint(0, len(revolver) - 1)] = True
async def ruletka(message: types.Message):
    global revolver
    shot = revolver.pop(0)
    if shot:
        await bot.send_message(message.chat.id, f"Выстрел!\n"
                                                f"@{message.from_user.username} "
                                                f"{message.from_user.first_name, message.from_user.last_name} "
                                                f"получает 5 минут бана!")
        revolver = [False] * 6
        revolver[randint(0, len(revolver) - 1)] = True
        is_admin = await bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
        if is_admin.status != "member":
            await bot.send_message(message.chat.id, f"Или нет...")
        else:
            ban_time = datetime.now() + timedelta(minutes=5)
            await bot.ban_chat_member(message.chat.id, message.from_user.id, ban_time)
    else:
        await bot.send_message(message.chat.id, f"Щелчок!")