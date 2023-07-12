from config import bot
from aiogram import types, Dispatcher
from database.sql_commands import Database
from aiogram.types import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup


async def list_of_users(call: types.CallbackQuery):
    users = Database().sql_select_user()
    if users:
        data = []
        for user in users:
            data.append(f'{user[0]}: '
                        f'id: {user[1]}\n'
                        f'user: {user[2]}\n'
                        f'фамилия и имя: {user[3]} {user[4]}\n')
        data = '\n'.join(data)
        await call.message.reply(f"{data}")
    else:
        await call.message.reply("Список пуст")


async def list_potential_user_ban(call: types.CallbackQuery):
    users = Database().select_potential_user_ban()
    if users:
        data = []
        for user in users:
            data.append(f'{user[0]}: '
                        f'id: {user[1]}\n'
                        f'user: {user[2]}\n'
                        f'фамилия и имя: {user[3]} {user[4]}\n'
                        f'дата: {user[5]}\n'
                        f'причина: {user[6]}\n')
        data = '\n'.join(data)
        await call.message.reply(f"{data}")
    else:
        await call.message.reply("Список пуст")

async def nothing(call: types.CallbackQuery):
    await call.message.reply(f"Нечего не придумал 😩")

def register_handlers_callback(dp: Dispatcher):
    dp.register_callback_query_handler(list_of_users, lambda call: call.data == "list_of_users")
    dp.register_callback_query_handler(list_potential_user_ban, lambda call: call.data == "list_potential_user_ban")
    dp.register_callback_query_handler(nothing, lambda call: call.data == "nothing")