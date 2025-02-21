import asyncio
import logging
import sys

from os import getenv
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReactionTypeEmoji

load_dotenv()
TOKEN = getenv("TOKEN")

dp = Dispatcher(storage=MemoryStorage())


# Команда /start
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет, {html.bold(message.from_user.full_name)}, это бот для реакции сообщений Кости")


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


# Команда /addEmojiReaction - Добавляем новую реакцию на сообщения пользователя
@dp.message(Command('addEmojiReaction'))
async def start_add_emoji_reaction(message: Message):
    logging.info("Команда /addEmojiReaction была вызвана.")
    await message.answer("Сообщение")


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
