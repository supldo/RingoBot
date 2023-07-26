from aiogram import types, Dispatcher
from config import bot
from database.sql_commands import Database
from datetime import datetime, timedelta
from config import admin

async def echo_ban(message: types.Message):
    ban_words = ["bitch", "damn", "fuck"]
    if message.chat.type == 'supergroup' and not message.from_user.id in admin:
        for word in ban_words:
            if word in message.text.lower().replace(" ", ''):
                if Database().sql_select_user_ban(message.from_user.id, message.chat.id):
                    ban_date = datetime.now() + timedelta(days=1)
                    await bot.ban_chat_member(message.chat.id, message.from_user.id, ban_date)
                    await bot.send_message(message.chat.id, f"Пользователь {message.from_user.first_name} был "
                                                            f"ограничен к чату на 1 день, за исползование мата в чате!")
                else:
                    await bot.send_message(message.chat.id, "Предупреждение! Использование ненормативной лексики "
                                                            "в чате, ограничевается доступ к чату!")
                Database().sql_insert_user_ban(message.from_user.id, message.chat.id, message.text)
                await bot.delete_message(
                    chat_id=message.chat.id,
                    message_id=message.message_id)