from database.sql_commands import Database
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import bot, admin

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

# Список пользователей
async def list_of_users(call: types.CallbackQuery):
    users = Database().sql_select_user()
    if users:
        for n in users:
            await bot.send_message(call.message.chat.id,
                            f'{users[n]["row_number"]}: '
                            f'ID: {users[n]["id"]}\n'
                            f'User: {users[n]["username"]}\n'
                            f'Фамилия: {users[n]["first_name"]}\n'
                            f'Имя: {users[n]["last_name"]}')
    else:
        await bot.send_message(call.message.chat.id, "Список пуст")


# Список потенциальных на бан
async def list_potential_user_ban(call: types.CallbackQuery):
    users = Database().select_potential_user_ban()
    if users:
        for n in users:
            await bot.send_message(call.message.chat.id,
                            f'{users[n]["row_number"]}: '
                            f'ID: {users[n]["id"]}\n'
                            f'User: {users[n]["username"]}\n'
                            f'Фамилия: {users[n]["first_name"]}\n'
                            f'Имя: {users[n]["last_name"]}\n'
                            f'Дата: {users[n]["datetime"]}\n'
                            f'Причина: {users[n]["rаeason"]}')
    else:
        await bot.send_message(call.message.chat.id, "Список пуст")


# Ответ пользователю
class SurveyAnswerStates(StatesGroup):
    survey_answer = State()
async def user_survey_answer(call: types.CallbackQuery, state: FSMContext):
    await bot.send_message(call.message.chat.id, "Напишите ответ пользователю")
    await SurveyAnswerStates.survey_answer.set()
    async with state.proxy() as data:
        data['user_survey_answer'] = call.message.reply_to_message.text

async def load_user_survey_answer(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        id_survey = data['user_survey_answer']
        survey = Database().sql_select_user_survey_by_id(int(id_survey))[int(id_survey)]
        await bot.send_message(survey['user_id'], f'Ответ от админа: {message.text}')
    await survey_answer.finish()

# Список опросов
class SurveyStates(StatesGroup):
    survey = State()

async def list_user_survey(call: types.CallbackQuery):
    surveys = Database().sql_select_user_survey()
    for n in surveys:
        await bot.send_message(call.message.chat.id,
                            f'ID Опроса: {surveys[n]["id"]}\n'
                            f'Идея: {surveys[n]["idea"]}\n'
                            f'Проблемы: {surveys[n]["problems"]}\n'
                            f'Оценка: {surveys[n]["assessment"]}\n'
                            f'ID Пользователя: {surveys[n]["user_id"]}')
    await bot.send_message(call.message.chat.id, "Выберите опрос по ID")
    await SurveyStates.survey.set()

# Опрос по ID
async def load_survey(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user_survey'] = message.text
    survey = Database().sql_select_user_survey_by_id(int(data['user_survey']))[int(data['user_survey'])]
    if survey:
        msg_result = f'ID Опроса: {int(data["user_survey"])}\n'\
                     f'Идея: {survey["idea"]}\n'\
                     f'Проблема: {survey["problems"]}\n'\
                     f'Оценка: {survey["assessment"]}\n'\
                     f'Пользователь: {survey["username"]}\n'\
                     f'Имя: {survey["first_name"]}\n'\
                     f'Фамилия: {survey["last_name"]}\n'\
                     f'ID Пользователя: {survey["user_id"]}'
        button_call_1 = InlineKeyboardButton(
            "Ответить",
            callback_data="user_survey_answer"
        )
        button_call_2 = InlineKeyboardButton(
            "Список опросов",
            callback_data="list_user_survey"
        )
        markup = InlineKeyboardMarkup().add(button_call_1, button_call_2)
        await message.reply(msg_result, reply_markup=markup)
        await state.finish()
    else:
        await bot.send_message(message.chat.id, 'Нечего не найдено!')

# Функции админа
async def secret_word(message: types.Message):
    if message.from_user.id in admin:
        markup = InlineKeyboardMarkup()
        button_call_1 = InlineKeyboardButton("Список пользователей", callback_data="list_of_users")
        markup.add(button_call_1)
        button_call_2 = InlineKeyboardButton("Список потеницальных пользователей на бан", callback_data="list_potential_user_ban")
        markup.add(button_call_2)
        button_call_3 = InlineKeyboardButton("Список опросов", callback_data="list_user_survey")
        markup.add(button_call_3)
        await message.reply("ZzZ...", reply_markup=markup)


# Диспетчер
def register_handler_admin(dp: Dispatcher):
    dp.register_message_handler(secret_word, lambda word: "Ringo" in word.text)
    dp.register_callback_query_handler(list_of_users, lambda call: call.data == "list_of_users")
    dp.register_callback_query_handler(list_potential_user_ban, lambda call: call.data == "list_potential_user_ban")
    dp.register_callback_query_handler(list_user_survey, lambda call: call.data == "list_user_survey")
    dp.register_callback_query_handler(user_survey_answer, lambda call: call.data == "user_survey_answer")
    dp.register_message_handler(load_survey, state=SurveyStates.survey, content_types=['text'])
    dp.register_message_handler(load_user_survey_answer, state=SurveyAnswerStates.survey_answer, content_types=['text'])