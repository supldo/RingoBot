from config import bot
from aiogram import types
from random import randint

async def random(message: types.Message):
    try:
        num_min, num_max = message.text.split()[1:]
        random = randint(int(num_min), int(num_max))
        await bot.send_message(message.chat.id, f'Случайное число: {random}')
    except:
        await bot.send_message(message.chat.id, 'Ошибка! Введите число от и до')