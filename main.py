from dotenv import load_dotenv
import logging
import os

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

# Создаем клавиатуру
menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

# Создаем кнопки-категории
category1 = KeyboardButton('Библиотека')
category2 = KeyboardButton('Помощь в выборе языка')
category3 = KeyboardButton('Изучение языка программирования')





# Добавляем кнопки на клавиатуру
menu_keyboard.add(category1, category2, category3)


# Configure logging
logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.send_message(message.chat.id, "Выберите категорию:", reply_markup=menu_keyboard)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)