from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import bot
from random import randint
from database.sql_commands import Database
from datetime import datetime, timedelta

async def secret_word(message: types.Message):
    markup = InlineKeyboardMarkup()
    button_call_1 = InlineKeyboardButton(
        "Список пользователей",
        callback_data="list_of_users"
    )
    markup.add(button_call_1)
    button_call_2 = InlineKeyboardButton(
        "Список потеницальных пользователей на бан",
        callback_data="list_potential_user_ban"
    )
    markup.add(button_call_2)
    button_call_3 = InlineKeyboardButton(
        "Nothing? 🤔",
        callback_data="nothing"
    )
    markup.add(button_call_3)
    if message.chat.id == 931619695:
        await message.reply("ZzZ...",
                            reply_markup=markup)

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

def register_handlers_chat_actions(dp: Dispatcher):
    dp.register_message_handler(secret_word, lambda word: "Ringo" in word.text)
    dp.register_message_handler(echo_ban)