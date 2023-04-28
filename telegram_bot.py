import logging
from dotenv import load_dotenv
import os
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
from aiogram.utils import executor
from categories import Categories
from roadmaps import RoadmapSelection
from chat import ChatGPT

load_dotenv()

class TelegramBot:
    def __init__(self, loop):
        self.bot_token = os.getenv('BOT_TOKEN')
        self.bot = Bot(token=self.bot_token)
        self.dp = Dispatcher(self.bot, loop=loop)
        self.categories = Categories()
        self.roadmap_selection = RoadmapSelection()
        logging.basicConfig(level=logging.INFO)

        self.register_handlers()

    def register_handlers(self):
        @self.dp.message_handler(commands=['start'])
        async def start_command(message: types.Message):
            await self.bot.send_message(message.chat.id, "Выберите категорию:", reply_markup=self.categories.menu_keyboard_with_subcategories)

        @self.dp.callback_query_handler(lambda query: query.data == 'category2')
        async def process_callback_category2(callback_query: types.CallbackQuery):
            language_selection = RoadmapSelection()
            await self.bot.send_message(callback_query.from_user.id, 'Выберите язык программирования:', reply_markup=language_selection.menu_keyboard)

        @self.dp.callback_query_handler(lambda query: query.data.startswith('roadmaps_'))
        async def process_callback_language(callback_query: types.CallbackQuery):
            lang = query.data.split('_')[1]
            # Здесь можно добавить обработку выбранного языка
            await self.bot.send_message(callback_query.from_user.id, f'Вы выбрали язык {lang}')
                      
    def start(self):
        executor.start_polling(self.dp, skip_updates=True)