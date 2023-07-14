from aiogram import types
from database.sql_commands import Database

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