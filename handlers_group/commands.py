# aiogram
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ContentType
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
# Database
from database.sql_commands import Database
# HELP
from handlers_group.const import HELP_TEXT
# modules
from random import randint
from datetime import datetime, timedelta
# keyboards
from keyboards import start_keyboard
# bot
from config import bot


# Команда START
async def start_button(message: types.Message):
    id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    Database().sql_insert_user(id=id,
                               username=username,
                               first_name=first_name,
                               last_name=last_name)
    await message.reply(text=f"Привет {message.from_user.first_name}!",
                        reply_markup=start_keyboard.start_markup)


# Команда HELP
async def help_button(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=HELP_TEXT)


# Жалоба
async def user_complaint(message: types.Message):
    text = message.text.split()
    telegram_id = int(message.from_user.id)
    telegram_id_bad_user = text[1][1:] if text[1][0] == "@" else text[1][0:]
    reason = " ".join(text[2:])
    count = 1
    bad_user = False

    username = Database().sql_select_user_query_by_username(user=telegram_id_bad_user).fetchall()
    first_name = Database().sql_select_user_query_by_first_name(user=telegram_id_bad_user).fetchall()
    last_name = Database().sql_select_user_query_by_last_name(user=telegram_id_bad_user).fetchall()

    if username:
        bad_user = username[0]
    elif first_name:
        bad_user = first_name[0]
    elif last_name:
        bad_user = last_name[0]

    complaint_check = Database().sql_select_complaint_table_check(user_id=telegram_id, bad_user_id=bad_user['id']).fetchall()

    if bad_user['id'] and bad_user['id'] != telegram_id:
        if complaint_check:
            await bot.send_message(chat_id=message.chat.id,
                                   text=f'Вы уже отправляли жалобу на {text[1]}')
        else:
            Database().sql_insert_complaint_table(telegram_id=telegram_id,
                                                  telegram_id_bad_user=bad_user['id'],
                                                  reason=reason,
                                                  count=count)

            await bot.send_message(chat_id=message.chat.id,
                                   text=f'Отправлено жалоба на {text[1]}')

            count_complaint = len(Database().sql_select_complaint_table(user_id=bad_user['id']).fetchall())

            if count_complaint >= 3:
                await bot.send_message(chat_id=bad_user['id'],
                                       text=f'На вас 3 раза пожаловались. '
                                            f'Вы исключены из группы Supido Group!')
                ban_date = datetime.now() + timedelta(days=365)
                await bot.ban_chat_member(message.chat.id, bad_user['id'], ban_date)
            else:
                await bot.send_message(chat_id=bad_user['id'],
                                       text=f'На вас пожаловались. '
                                            f'Ещё {3 - count_complaint} жалоба и вас исключат из группы!')


# Викторина
quiz_id = None
async def quiz_1(message: types.Message):
    global quiz_id
    quiz_id = 'quiz_1'
    question = "Ну тип это опрос 1"
    option = [
        "Вариант А",
        "Правильный вариант",
        "Вариант 3",
        "Что?"
    ]
    markup = InlineKeyboardMarkup()
    button_call_1 = InlineKeyboardButton(
        "Следующая викторина",
        callback_data="button_call_1"
    )
    markup.add(button_call_1)
    await bot.send_poll(
        chat_id=message.chat.id,
        question=question,
        options=option,
        is_anonymous=False,
        type='quiz',
        correct_option_id=1,
        explanation="Правильный ответ 2",
        explanation_parse_mode=types.ParseMode.MARKDOWN_V2,
        reply_markup=markup
    )
async def quiz_2(call: types.PollAnswer):
    global quiz_id
    quiz_id = 'quiz_2'
    question = "А тип следующий опрос, верно же?"
    option = [
        "Вариант В",
        "Точно неправильный вариант",
        "А это точно правильный вариант",
        "Да-да, верхниый точно правильный вариант"
    ]
    await bot.send_poll(
        chat_id=call.message.chat.id,
        question=question,
        options=option,
        is_anonymous=False,
        type='quiz',
        correct_option_id=2,
        explanation="Правильный ответ 3",
        explanation_parse_mode=types.ParseMode.MARKDOWN_V2
    )
async def handle_poll_answer(poll_answer: types.PollAnswer):
    Database().sql_insert_answers_quiz(id_user=poll_answer.user.id,
                                       quiz=quiz_id,
                                       quiz_option=poll_answer.option_ids[0])


# Игра Русская рулетка
revolver = [False] * 6
revolver[randint(0, len(revolver) - 1)] = True
async def ruletka(message: types.Message):
    global revolver
    shot = revolver.pop(0)
    if shot:
        await bot.send_message(message.chat.id, f"Выстрел!\n"
                                                f"@{message.from_user.username} "
                                                f"{message.from_user.first_name, message.from_user.last_name} "
                                                f"получает 5 минут бана!")
        revolver = [False] * 6
        revolver[randint(0, len(revolver) - 1)] = True
        is_admin = await bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
        if is_admin.status != "member":
            await bot.send_message(message.chat.id, f"Или нет...")
        else:
            ban_time = datetime.now() + timedelta(minutes=5)
            await bot.ban_chat_member(message.chat.id, message.from_user.id, ban_time)
    else:
        await bot.send_message(message.chat.id, f"Щелчок!")


# Рандомное число
async def random(message: types.Message):
    try:
        num_min, num_max = message.text.split()[1:]
        random = randint(int(num_min), int(num_max))
        await bot.send_message(message.chat.id, f'Случайное число: {random}')
    except:
        await bot.send_message(message.chat.id, 'Ошибка! Введите число от и до')


# Узнать свой ID
async def user_id(message: types.Message):
    await bot.send_message(message.chat.id, f'Ваш ID: {message.from_user.id}')


# Идеи и отзывы от пользователя
class FormStates(StatesGroup):
    idea = State()
    problems = State()
    assessment = State()
    user_id = State()
async def fsm_start(message: types.Message):
    await message.reply("Здрасти! Дайти идия! Ато фанзтазия не робит")
    await FormStates.idea.set()
async def load_idea(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['idea'] = message.text
    await FormStates.next()
    await message.reply("Э! Кста, у тебя побремы какие-то против моего бота!?")
async def load_problems(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['problems'] = message.text
    await FormStates.next()
    await message.reply("Оценишь моего бота 10 из 10?")
async def load_assessment(message: types.Message, state: FSMContext):
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


# Dispatcher
def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_button, commands=['start'])
    dp.register_message_handler(help_button, commands=['help'])
    dp.register_message_handler(user_complaint, commands=['complaint'])
    dp.register_message_handler(quiz_1, commands=['quiz'])
    dp.register_callback_query_handler(quiz_2, lambda call: call.data == "button_call_1")
    dp.register_poll_answer_handler(handle_poll_answer)
    dp.register_message_handler(random, commands=['random'])
    dp.register_message_handler(user_id, commands=['my_id'])
    dp.register_message_handler(ruletka, commands=['ruletka'])
    dp.register_message_handler(fsm_start, commands=['survey'])
    dp.register_message_handler(load_idea, state=FormStates.idea, content_types=['text'])
    dp.register_message_handler(load_problems, state=FormStates.problems, content_types=['text'])
    dp.register_message_handler(load_assessment, state=FormStates.assessment, content_types=['text'])