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
from database.database import Database
import sqlite3

load_dotenv()

class TelegramBot:
    def __init__(self, loop):
        self.bot_token = os.environ['BOT_TOKEN']
        self.bot = Bot(token=self.bot_token)
        self.dp = Dispatcher(self.bot, loop=loop)
        self.categories = Categories()
        self.roadmap_selection = RoadmapSelection()
        self.openai_api_key = os.environ['CHATGPT_API_TOKEN']
        self.chat_gpt = ChatGPT(bot_token=self.bot_token, loop=loop)
        self.db = Database('database/users.db') 

        # Initialize session variable to keep track of logged in users
        self.logged_in_users = set()

        logging.basicConfig(level=logging.INFO)

        self.register_handlers()

    def register_handlers(self):
        @self.dp.message_handler(commands=['start'])
        async def start_command(message: types.Message):
            await self.bot.send_message(message.chat.id, "Добро пожаловать! Нажмите кнопку 'Войти', чтобы начать.", reply_markup=self.categories.login_button_keyboard())

        @self.dp.message_handler(lambda message: message.text == 'Войти')
        async def login_handler(message: types.Message):
            user_id = message.from_user.id
            self.cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
            existing_user = self.cursor.fetchone()

            if existing_user is None:
                self.db.insert_user(user_id, message.from_user.first_name, message.from_user.username)
                await self.bot.send_message(message.chat.id, f"Вы вошли в систему под идентификатором {user_id}.")
            else:
                await self.bot.send_message(message.chat.id, f"Вы уже вошли в систему под идентификатором {user_id}.")
            
            # Отправка клавиатуры с категориями пользователю, если он уже залогинен
            if user_id in self.logged_in_users:
                await self.bot.send_message(message.chat.id, "Выберите категорию:", reply_markup=self.categories.menu_keyboard_with_subcategories())

        @self.dp.callback_query_handler(lambda query: query.data == 'category_roadmaps')
        async def process_callback_roadmap(callback_query: types.CallbackQuery):
            user_id = callback_query.from_user.id
            if user_id not in self.logged_in_users:
                await self.bot.send_message(user_id, "Вы не авторизованы. Нажмите кнопку 'Войти', чтобы начать.")
                return
            language_selection = RoadmapSelection()
            await self.bot.send_message(user_id, 'Выберите язык программирования:', reply_markup=language_selection.menu_keyboard)

        @self.dp.callback_query_handler(lambda query: query.data.startswith('roadmaps_'))
        async def process_callback_language(callback_query: types.CallbackQuery):
            lang = self.query.data.split('_')[1]
            # Здесь можно добавить обработку выбранного языка
            await self.bot.send_message(callback_query.from_user.id, f'Вы выбрали язык {lang}')

        @self.dp.callback_query_handler(lambda query: query.data == 'category_chat')
        async def process_callback_chatgpt(callback_query: types.CallbackQuery):
            # Clear previous message buttons
            await self.bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id, reply_markup=None)
            # Send welcome message and back button
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Назад'))
            await self.bot.send_message(callback_query.from_user.id, 'Добро пожаловать в чат!', reply_markup=keyboard)
            # Register handler for back button
            @self.dp.message_handler(lambda message: message.text == 'Назад')
            async def process_callback_back(message: types.Message):
                await self.bot.send_message(message.chat.id, '', reply_markup=self.categories.menu_keyboard_with_subcategories())
                # Remove the back button handler
                self.dp.remove_handler(process_callback_back)
            # Register handler for incoming chat messages
            @self.dp.message_handler(content_types=types.ContentType.TEXT)
            async def process_chat_message(message: types.Message):
                response = await self.chat_gpt.generate_response(message.text)
                await self.bot.send_message(chat_id=message.chat.id, text=response)
            # Wait for chat messages or back button
            await self.dp.wait_for(self.dp.message_handlers, timeout=60.0)
            # Remove the chat message handler
            self.dp.remove_handler(process_chat_message)

    def start(self):
        executor.start_polling(self.dp, skip_updates=True)