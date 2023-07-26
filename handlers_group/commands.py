# modules
import asyncio
from binascii import hexlify
from os import urandom
from random import randint
from datetime import datetime, timedelta
# aiogram
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ContentType
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.deep_linking import _create_link
# Database
from database.sql_commands import Database
# HELP
from handlers_group.const import HELP_TEXT
# keyboards
from keyboards import start_keyboard
# bot
from config import bot
# echo ban
from handlers_group.echo_ban import echo_ban
# anime search
import handlers_group.scraper_anime as rec

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
    Database().sql_insert_wallet(id)
    await message.reply(text=f"Привет {message.from_user.first_name}!",
                        reply_markup=start_keyboard.start_markup)

    if len(message.text.split()) > 1: await referral_check(message.text.split()[1], message)


# Обработчик кнопок
async def button_handler(message: types.Message):
    kb = start_keyboard
    tx = message.text
    if kb.help_button["text"] == tx:
        await help_button(message)
    elif kb.wallet_button["text"] == tx:
        await wallet(message)
    elif kb.referrals_button["text"] == tx:
        await referrals(message)
    elif kb.reference_button["text"] == tx:
        await reference_link(message)
    elif kb.random_button["text"] == tx:
        await random(message)
    elif kb.quiz_button["text"] == tx:
        await quiz_1(message)
    elif kb.ruletka_button["text"] == tx:
        await ruletka(message)
    elif kb.help_anime['text'] == tx:
        await help_recommend_anime(message)
    elif kb.anime['text'] == tx:
        await recommend_anime(message)
    elif kb.anime_anons['text'] == tx:
        await recommend_anime(message, status_anime='anons')
    elif kb.anime_ongoing['text'] == tx:
        await recommend_anime(message, status_anime='ongoing')
    elif kb.anime_year['text'] == tx:
        await recommend_anime(message, status_anime='released', season_anime='2023')
    elif kb.anime_note['text'] == tx:
        await anime_note(message)
    else:
        await echo_ban(message)


# Команда HELP
async def help_button(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=HELP_TEXT)


# Проверка реферальной ссылки
async def referral_check(referral, message):
    user_id = Database().sql_select_user_by_link(f'%{referral}')[0]['link']
    if user_id == message.from_user.id:
        await bot.send_message(message.chat.id, 'Нельзя приглашать самого себя! 🙃')
    elif not Database().sql_select_referral(message.from_user.id):
        Database().sql_insert_referral(user_id, message.from_user.id)
        Database().sql_update_wallet(user_id)
        await bot.send_message(user_id, f'Пользователеь зашёл через вашу реферальную ссылку, к вам зачислено +100 баллов\n'
                                        f'Свои баллы можете посмотреть через команду: /wallet')


# Реферальная ссылка
async def reference_link(message: types.Message):
    link_exist = Database().sql_select_user_return_link(telegram_id=message.from_user.id)
    link = link_exist[0]["link"]
    if link:
        await bot.send_message(chat_id=message.from_user.id,
                               text=f"У тебя уже есть реферальная ссылка!\n"
                                    f"Ссылка: {link}")
    else:
        code = hexlify(urandom(4)).decode()
        link = await _create_link(link_type="start", payload=code)
        Database().sql_update_user_reference_link(link=link, telegram_id=message.from_user.id)
        await bot.send_message(message.from_user.id,
                               f"Твоя реферальная ссылка: {link}")


# Список рефералов
async def referrals(message: types.Message):
    referrals = Database().sql_select_all_referrals(message.from_user.id)
    if referrals:
        show_referrals = ''
        for referral in referrals:
            user_n = lambda x: x if x is not None else ""
            referral_list = [f"{user_n(referral['id']):}",
                             user_n(referral['username']),
                             user_n(referral['first_name']),
                             user_n(referral['last_name'])]
            referral_str = ' '.join(referral_list)
            show_referrals += referral_str
        await bot.send_message(message.chat.id, show_referrals)
    else:
        await bot.send_message(message.chat.id, 'У вас пока нету рефераллов')


# Кошелёк
async def wallet(message: types.Message):
    point = Database().sql_select_wallet(message.from_user.id)
    await message.reply(f'На вашем счету: {point} баллов')


# Жалоба
async def user_complaint(message: types.Message):
    text = message.text.split()

    telegram_id = int(message.from_user.id)
    telegram_id_bad_user = text[1][1:] if text[1][0] == "@" else text[1][0:]
    reason = " ".join(text[2:])
    count = 1
    bad_user = {'id': False}

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

    if complaint_check:
        await bot.send_message(chat_id=message.chat.id,
                               text=f'Вы уже отправляли жалобу на {text[1]}')
    elif bad_user['id'] == telegram_id:
        await bot.send_message(chat_id=message.chat.id,
                               text=f'Не стоит на себя жаловатся! 🙃')
    elif bad_user['id']:
        Database().sql_insert_complaint_table(telegram_id=telegram_id,
                                              telegram_id_bad_user=bad_user['id'],
                                              reason=reason,
                                              count=count)

        await bot.send_message(chat_id=message.chat.id,
                               text=f'Отправлено жалоба на {text[1]}')

        count_complaint = len(Database().sql_select_complaint_table(user_id=bad_user['id']).fetchall())
        try:
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
        except:
            print('Пользователь остановил общение с ботом.')
    else:
        await bot.send_message(chat_id=message.chat.id,
                               text=f'Такой пользователь не найден')


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
    if message.chat.type == 'supergroup':
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
    else:
        await bot.send_message(message.chat.id, f"Русская рулетка работает только в группе")


# Рандомное число
async def random(message: types.Message):
    num_list = list(map(int, [num for num in message.text.split() if num.isdigit()]))
    if len(num_list) == 1:
        random = randint(1, num_list[0])
    elif len(num_list) == 2:
        random = randint(min(num_list), max(num_list))
    else:
        random = randint(1, 100)
    await bot.send_message(message.chat.id, f'Случайное число: {random}')


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


# Совет аниме
async def help_recommend_anime(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text=f"Привет {message.from_user.first_name}!",
                           reply_markup=start_keyboard.anime_markup)
async def recommend_anime(message: types.Message, status_anime=None, season_anime=None):
    command = message.text.split()
    statuses = ['anons', 'released', 'ongoing']

    if len(command) > 1:
        if command[1] in statuses:
            status_anime = command[1]
        elif command[1].isdigit():
            if 1990 <= int(command[1]) and int(command[1]) <= 2023:
                status_anime = 'released'
                season_anime = command[1]

    anime_link = rec.recommend(status=status_anime, season=season_anime)

    anime = rec.recommend_print(anime_link)

    recommend = f"{anime['title']}\n" \
                f"{anime['rating']}\n" \
                f"{anime['episodes']}\n" \
                f"{anime['date_release']}\n" \
                f"{anime['genres']}\n\n" \
                f"{anime['description']}"
    if len(recommend) >= 1024:
        recommend = recommend[:1021] + "..."

    markup = InlineKeyboardMarkup()
    anime_note = InlineKeyboardButton(
        "Добавить в заметки",
        callback_data="save_anime_note"
    )
    markup.add(anime_note)

    await bot.send_photo(chat_id=message.chat.id,
                         photo=anime['image'],
                         caption=recommend,
                         parse_mode=types.ParseMode.MARKDOWN,
                         reply_markup=markup)
async def save_anime_note(call: types.CallbackQuery, state: FSMContext):
    await bot.send_message(chat_id=call.message.chat.id, text='Добавлено в заметки')
    async with state.proxy() as data:
        Database().sql_insert_anime_note(call.from_user.id, data['link'])
        print(data['link'])
async def anime_note(message: types.Message):
    anime_note = Database().sql_select_anime_note(message.from_user.id)
    for anime_link in anime_note:
        anime = rec.recommend_print('https://shikimori.me/animes/' + anime_link['link'])
        recommend = f"{anime['title']}\n" \
                    f"{anime['rating']}\n" \
                    f"{anime['episodes']}\n" \
                    f"{anime['date_release']}\n" \
                    f"{anime['genres']}\n\n" \
                    f"{anime['description']}"
        if len(recommend) >= 1024:
            recommend = recommend[:1021] + "..."

        await bot.send_photo(chat_id=message.chat.id,
                             photo=anime['image'],
                             caption=recommend,
                             parse_mode=types.ParseMode.MARKDOWN)


# Dispatcher
def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_button, commands=['start'])
    dp.register_message_handler(help_button, commands=['help'])
    dp.register_message_handler(help_recommend_anime, commands=['help_anime'])
    dp.register_message_handler(recommend_anime, commands=['anime'])
    dp.register_message_handler(anime_note, commands=['anime_note'])
    dp.register_callback_query_handler(save_anime_note, lambda call: call.data == "save_anime_note")
    dp.register_message_handler(reference_link, commands=['reference'])
    dp.register_message_handler(referrals, commands=['referrals'])
    dp.register_message_handler(user_complaint, commands=['complaint'])
    dp.register_message_handler(wallet, commands=['wallet'])
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
    dp.register_message_handler(button_handler)
