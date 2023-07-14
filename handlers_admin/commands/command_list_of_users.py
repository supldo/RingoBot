from aiogram import types
from database.sql_commands import Database

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