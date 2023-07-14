from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import bot, admin

async def secret_word(message: types.Message):
    if message.from_user.id in admin:
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
            "Список опросов",
            callback_data="list_user_survey"
        )
        markup.add(button_call_3)
        button_call_3 = InlineKeyboardButton(
            "Nothing? 🤔",
            callback_data="nothing"
        )
        markup.add(button_call_3)

        await message.reply("ZzZ...", reply_markup=markup)


def register_handlers_chat_actions(dp: Dispatcher):
    dp.register_message_handler(secret_word, lambda word: "Ringo" in word.text)