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


# Команда /addReactionEvent - Добавляем новую реакцию на сообщения пользователя
@dp.message(Command('addReactionEvent'))
async def add_emoji_reaction(message: Message):
    logging.info("Команда /addReactionEvent была вызвана.")

    # Извлекаем текст сообщения после команды
    args = message.text.strip().split()

    await message.answer(str(len(args)))

    """if len(args) != 2:
        await message.answer("Неверное количество параметров. Используйте:\n"
                            "/addReactionEvent <emoji> <event_duration>")
        return"""

    # Фиксируем айди чата
    chat_id = message.chat.id

    # Фиксируем айди пользователя по пересланному сообщению
    user_id = get_tg_id(message)

    # Фиксируем смайлик для буллинга
    if is_available_emoji(args[1]):
        emoji  = is_available_emoji(args[1])
    else:
        await message.answer("Смайлик для реакций не допустим!")
        return

    # Фиксируем длину ивента
    await message.answer(args[2])

    if transfer_interval(args[2]):
        event_duration = transfer_interval(args[2])
    else:
        await message.answer("Некорректная длительность ивента: \n"
                             "- Длительность ивента должна быть в формате МИНУТЫ:СЕКУНДЫ; \n"
                             "- Длительность ивента должна быть меньше часа.")
        return


    # Фиксируем начала ивента
    event_start = message.date

    insert_reaction_event(chat_id, user_id, emoji, event_duration, event_start)

    await message.answer(f"Добавлено событие реакции:\n"
                        f"Chat ID: {chat_id}\n"
                        f"User ID: {user_id}\n"
                        f"Emoji: {emoji}\n"
                        f"Event Duration: {event_duration}\n"
                        f"Start Event: {event_start}")


# Обработчик любого сообщения
@dp.message()
async def update_user_data(message: Message) -> None:
    """ user_id = message.from_user.id  # получаем айди пользователя
    # Костя - 992948178
    # Я - 7044405837
    if user_id == 992948178:
        emoji = ReactionTypeEmoji(emoji='🤓')
        try:
            await message.react([emoji])
        except Exception as e:
            print(f"Ошибка при добавлении реакции: {e}")"""


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
