from aiogram import types

async def nothing(call: types.CallbackQuery):
    await call.message.reply(f"Нечего не придумал 😩")