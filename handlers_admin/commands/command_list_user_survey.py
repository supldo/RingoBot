from aiogram import Dispatcher, types
from config import bot
from database.sql_commands import Database
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ContentType
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class FormStates(StatesGroup):
    survey = State()

async def list_user_survey(call: types.CallbackQuery):
    surveys = Database().sql_select_user_survey()
    send_msg = ''
    for survey in surveys:
        send_msg += f'id: {survey[0]}\n'\
                   f'идея: {survey[1]}\n'\
                   f'проблемы: {survey[2]}\n'\
                   f'оценка: {survey[3]}\n\n'
    await bot.send_message(call.message.chat.id, send_msg)
    await bot.send_message(call.message.chat.id, "Выберите опрос по ID")
    await FormStates.survey.set()

async def load_survey(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user_survey'] = message.text

    survey = Database().sql_select_user_survey_by_id(int(data['user_survey']))

    if survey:
        msg_result = f'идея: {survey[0][1]}\n'\
                     f'проблемы: {survey[0][2]}\n'\
                     f'оценка: {survey[0][3]}\n'\
                     f'пользователь: {survey[0][6]}\n'\
                     f'имя: {survey[0][7]}\n'\
                     f'фамилия: {survey[0][8]}\n'\
                     f'id пользователя: {survey[0][5]}'

        markup = InlineKeyboardMarkup()
        button_call_1 = InlineKeyboardButton(
            "Кнопка 1",
            callback_data="list_of_users"
        )
        markup.add(button_call_1)
        button_call_2 = InlineKeyboardButton(
            "Кнопка 2",
            callback_data="list_potential_user_ban"
        )
        markup.add(button_call_2)
        await message.reply(msg_result, reply_markup=markup)

    else:
        await bot.send_message(message.chat.id, 'Нечего не найдено!')

def register_handler_load_survey(dp: Dispatcher):
    dp.register_message_handler(load_survey, state=FormStates.survey, content_types=['text'])