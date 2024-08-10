import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from database import create_table, update_quiz_index_score, get_quiz_index, get_quiz_score, get_all_quiz_stats
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from questions import quiz_data

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)

# Замените "YOUR_BOT_TOKEN" на токен, который вы получили от BotFather
API_TOKEN = '7472297360:AAHuPW2CGwewP9H4GrZ6mBzXBsYx-7Pee6A'

# Объект бота
bot = Bot(token=API_TOKEN)
# Диспетчер
dp = Dispatcher()


# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # Создаем сборщика клавиатур типа Reply
    builder = ReplyKeyboardBuilder()
    # Добавляем в сборщик одну кнопку
    builder.add(types.KeyboardButton(text="Начать игру"))
    # Прикрепляем кнопки к сообщению
    await message.answer("Добро пожаловать в квиз!", reply_markup=builder.as_markup(resize_keyboard=True))


# Хэндлер на команды /quiz
@dp.message(F.text == "Начать игру")
@dp.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
    # Отправляем новое сообщение без кнопок
    await message.answer(f"Давайте начнем квиз!")
    # Запускаем новый квиз
    await new_quiz(message)


async def new_quiz(message):
    # получаем id пользователя, отправившего сообщение
    user_id = message.from_user.id
    # сбрасываем значение текущего индекса вопроса квиза и результата в 0
    current_question_index = 0
    score = 0
    await update_quiz_index_score(user_id, current_question_index, score)

    # запрашиваем новый вопрос для квиза
    await get_question(message, user_id)


async def get_question(message, user_id):
    # Запрашиваем из базы текущий индекс для вопроса
    current_question_index = await get_quiz_index(user_id)
    # Получаем индекс правильного ответа для текущего вопроса
    correct_index = quiz_data[current_question_index]['correct_option']
    # Получаем список вариантов ответа для текущего вопроса
    opts = quiz_data[current_question_index]['options']

    # Функция генерации кнопок для текущего вопроса квиза
    # В качестве аргументов передаем варианты ответов и значение правильного ответа (не индекс!)
    kb = generate_options_keyboard(opts, opts[correct_index])
    # Отправляем в чат сообщение с вопросом, прикрепляем сгенерированные кнопки
    await message.answer(f"{quiz_data[current_question_index]['question']}", reply_markup=kb)


def generate_options_keyboard(answer_options, right_answer):
    # Создаем сборщика клавиатур типа Inline
    builder = InlineKeyboardBuilder()

    # В цикле создаем 4 Inline кнопки, а точнее Callback-кнопки
    for ind, option in enumerate(answer_options):
        builder.add(types.InlineKeyboardButton(
            # Текст на кнопках соответствует вариантам ответов
            text=option,
            # Присваиваем данные для колбэк запроса.
            # Если ответ верный сформируется колбэк-запрос с данными 'right_answer'
            # Если ответ неверный сформируется колбэк-запрос с данными 'wrong_answer'
            callback_data=f'{ind}|{"right_answer" if option == right_answer else "wrong_answer"}')
        )

    # Выводим по одной кнопке в столбик
    builder.adjust(1)
    return builder.as_markup()


@dp.callback_query(lambda c: True)
async def right_wrong_answer(callback: types.CallbackQuery):
    # редактируем текущее сообщение с целью убрать кнопки (reply_markup=None)
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    # Получение текущего вопроса для данного пользователя
    current_question_index = await get_quiz_index(callback.from_user.id)

    user_index, answer_type = callback.data.split('|')
    await callback.message.answer(f"{quiz_data[current_question_index]['options'][int(user_index)]}")
    score = 0
    if answer_type == 'right_answer':
        # Отправляем в чат сообщение, что ответ верный
        await callback.message.answer("Верно!")
        score = 1
    else:
        correct_option = quiz_data[current_question_index]['correct_option']
        # Отправляем в чат сообщение об ошибке с указанием верного ответа
        await callback.message.answer(
            f"Неправильно. Правильный ответ: {quiz_data[current_question_index]['options'][correct_option]}")

    # Обновление номера текущего вопроса в базе данных
    current_question_index += 1
    last_score = await get_quiz_score(callback.from_user.id)
    total_score = (last_score or 0) + score
    await update_quiz_index_score(callback.from_user.id, current_question_index, total_score)
    # Проверяем достигнут ли конец квиза
    if current_question_index < len(quiz_data):
        # Следующий вопрос
        await get_question(callback.message, callback.from_user.id)
    else:
        # Уведомление об окончании квиза
        score = await get_quiz_score(callback.from_user.id)
        await callback.message.answer(f"Это был последний вопрос. Квиз завершен! \nВаш результат {score}/10")
        await show_all_quiz_stats(callback.message,callback.from_user.id)


async def show_all_quiz_stats(message,user_id):
    stats = await get_all_quiz_stats()
    if not stats:
        await message.answer("Нет статистики игроков.")
        return

    statistics_message = "Статистика игроков:\n"
    for stat in stats:
        if stat['user_id'] == user_id:
            statistics_message += (f"Вы: "
                                   f"Последний результат: {stat['last_score']}\n")
        else:
            statistics_message += (f"{stat['user_id']}: "
                               f"Последний результат: {stat['last_score']}\n")

    await message.answer(statistics_message)



# Запуск процесса поллинга новых апдейтов
async def main():
    # Запускаем создание таблицы базы данных
    await create_table()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
