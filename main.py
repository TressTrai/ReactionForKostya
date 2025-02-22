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

    if len(args) != 3:
        await message.reply("Неверное количество параметров.\n"
                            "Используйте: /addReactionEvent эмодзи длительность_ивента")
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
    event_start = message.date

    # Проверяем на то, что на данного пользователя еще нет ивента
    reaction_keys = [(item[0], item[1]) for item in get_reaction_event()]

    if (chat_id, user_id) in reaction_keys:
        await message.reply("Ивент на данного пользователя в текущем чате уже идет!")
        return


    insert_reaction_event(chat_id, user_id, emoji, event_duration, event_start)

    await message.reply(f"Добавлено событие реакции:\n"
                        f"Chat ID: {chat_id}\n"
                        f"User ID: {user_id}\n"
                        f"Emoji: {emoji}\n"
                        f"Event Duration: {event_duration}\n"
                        f"Start Event: {event_start}")


# Обработчик любого сообщения
@dp.message()
async def check_message(message: Message) -> None:
    # получаем айди чата
    chat_id = message.chat.id

    # получаем айди пользователя
    user_id = message.from_user.id

    # Костя - 992948178
    # Я - 7044405837
    """if user_id == 992948178:
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
