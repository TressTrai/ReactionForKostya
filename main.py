import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReactionTypeEmoji

from SQL_Queries import *

from check_functions import *

load_dotenv()

TOKEN = getenv("TOKEN")

dp = Dispatcher(storage=MemoryStorage())

# Команда /start
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет, {html.bold(message.from_user.full_name)}, это бот для простановки реакций сообщений "
                         f"Пользователей")


# Команда /help - Бот объясняет как он работает
@dp.message(Command('help'))
async def print_help(message: Message):
    await message.reply("Чтобы создать ивент реакций на пользователя необходимо:\n"
                         "1) Выбрать жертву \n"
                         "2) Найти его сообщение в текущем чате\n"
                         "3) Ответить на его сообщение\n"
                         "4) Ввести команду /add_event\n"
                         "5) Через пробел указать необходимый эмодзи для реакции\n"
                         "6) Через пробел указать длительность ивента в формате МИНУТЫ:СЕКУНДЫ\n"
                         "7) Наслаждаться")

# Команда /addReactionEvent - Добавляем новую реакцию на сообщения пользователя
@dp.message(Command('add_event'))
async def add_emoji_reaction(message: Message):

    # Извлекаем текст сообщения после команды
    args = message.text.strip().split()

    if len(args) != 3:
        await message.reply("Неверное количество параметров.\n"
                            "Используйте: /add_event эмодзи длительность_ивента")
        return

    # Фиксируем айди чата
    chat_id = message.chat.id

    # Фиксируем айди пользователя по пересланному сообщению
    user_id = get_tg_id(message)

    # Фиксируем смайлик для буллинга
    if is_available_emoji(args[1]):
        emoji  = is_available_emoji(args[1])
    else:
        await message.reply("Смайлик для реакций не допустим!")
        return

    # Фиксируем длину ивента
    if transfer_interval(args[2]):
        event_duration = transfer_interval(args[2])
    else:
        await message.reply("Некорректная длительность ивента: \n"
                             "- Длительность ивента должна быть в формате МИНУТЫ:СЕКУНДЫ; \n"
                             "- Длительность ивента должна быть меньше часа.")
        return


    # Фиксируем начала ивента
    event_start = str(message.date).replace("+00:00", "")

    # Проверяем на то, что на данного пользователя еще нет ивента
    reaction_keys = [(item[0], item[1]) for item in get_reaction_event()]

    if (chat_id, user_id) in reaction_keys:
        await message.reply("Ивент на данного пользователя в текущем чате уже идет!")
        return


    insert_reaction_event(chat_id, user_id, emoji, event_duration, event_start)

    user_fullname = get_tg_fullname(message)

    await message.reply(
        f"Добавлен новый ивент в этом чате:\n"
        f"Для пользователя: <a href=\"tg://user?id={user_id}\">{user_fullname}</a>\n"
        f"Эмодзи-реакция: {emoji}\n"
        f"Длительность: {event_duration.replace("m", " минут").replace("s", " секунд")}\n",
    )
    # f"Длительность: {event_duration.split(":")[0]} минут {event_duration.split(":")[1]} секунд\n")

    """await message.reply(f"Добавлено событие реакции:\n"
                        f"Chat ID: {chat_id}\n"
                        f"User ID: {user_id}\n"
                        f"Emoji: {emoji}\n"
                        f"Event Duration: {event_duration}\n"
                        f"Start Event: {event_start}")"""


# Обработчик любого сообщения
@dp.message()
async def check_message(message: Message) -> None:
    # получаем айди чата
    chat_id = message.chat.id

    # получаем айди пользователя
    user_id = message.from_user.id

    # Пасхалка для деда
    if chat_id == -1001781232071 and user_id == 804111143:
        text = message.text.lower()  # Приводим текст к нижнему регистру
        if text == "пизда":
            await message.reply("Да.")
        if text == "да":
            await message.reply("Пизда.")
        if "питон" in text:
            await message.reply("Питон говно.")

    # получаем все ивенты
    reaction_events = get_reaction_event()

    reaction_keys = [(item[0], item[1]) for item in reaction_events]

    # проверяем есть ли ивент для данного пользователя в данном чате
    if not (chat_id, user_id) in reaction_keys:
        return

    # перебираем все ивенты
    for event in reaction_events:

        # находим нужный ивент
        if event[0] == chat_id and event[1] == user_id:

            # Проверяем закончился ли ивент
            if event[3] + event[4] < message.date.replace(tzinfo=None):
                # Удаляем ивент, если он закончен
                delete_reaction_event(chat_id, user_id)
                return

            # Наконец-то ставим какую-то реакцию
            emoji = ReactionTypeEmoji(emoji=event[2])

            try:
                await message.react([emoji])
            except Exception as e:
                print(f"Ошибка при добавлении реакции: {e}")


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped!")
