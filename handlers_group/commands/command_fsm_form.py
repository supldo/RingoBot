from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ContentType

from config import bot
from database.sql_commands import Database


class FormStates(StatesGroup):
    idea = State()
    problems = State()
    assessment = State()
    user_id = State()


async def fsm_start(message: types.Message):
    await message.reply("Здрасти! Дайти идия! Ато фанзтазия не робит")
    await FormStates.idea.set()

async def load_idea(message: types.Message,
                        state: FSMContext):
    async with state.proxy() as data:
        data['idea'] = message.text
    await FormStates.next()
    await message.reply("Э! Кста, у тебя побремы какие-то против моего бота!?")


async def load_problems(message: types.Message,
                        state: FSMContext):
    async with state.proxy() as data:
        data['problems'] = message.text
    await FormStates.next()
    await message.reply("Оценишь моего бота 10 из 10?")


async def load_assessment(message: types.Message,
                        state: FSMContext):
    async with state.proxy() as data:
        if message.text.isdigit() and int(message.text) == 10:
            await message.reply("А хотя, давай 100 из 10? Да, пусть 100 из 10")
            await bot.send_message(message.chat.id, "Давай я вместо тебя запишу")
            await bot.send_message(message.chat.id, "А ты свободен, можешь идти")
            Database().sql_insert_user_survey(
                idea=data['idea'],
                problems=data['problems'],
                assessment=100,
                user_id=message.from_user.id
            )
            await state.finish()
        else:
            await message.reply("Я вроде чётко сказал, оценить 10 из 10!")


def register_handler_fsm_form(dp: Dispatcher):
    dp.register_message_handler(fsm_start, commands=['survey'])
    dp.register_message_handler(load_idea, state=FormStates.idea, content_types=['text'])
    dp.register_message_handler(load_problems, state=FormStates.problems, content_types=['text'])
    dp.register_message_handler(load_assessment, state=FormStates.assessment, content_types=['text'])
