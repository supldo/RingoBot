from aiogram import types, Dispatcher
from config import bot
from database.sql_commands import Database
from datetime import datetime, timedelta

async def echo_ban(message: types.Message):
    is_admin = await bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
    ban_words = ["bitch", "damn", "fuck"]
    if message.chat.id == -1001835217444 and is_admin.status == "member":
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


def register_handlers_echo_ban(dp: Dispatcher):
    dp.register_message_handler(echo_ban)