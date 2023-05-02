import openai
import os
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.environ['CHATGPT_API_TOKEN']

class ChatGPT:
    def __init__(self, bot_token, loop):
        self.bot_token = bot_token
        self.bot = Bot(token=self.bot_token, loop=loop)
        self.dp = Dispatcher(self.bot, loop=loop)
        self.register_handlers()
        self.openai_api_key = os.environ['CHATGPT_API_TOKEN']
        openai.api_key = self.openai_api_key

    def register_handlers(self):
        @self.dp.message_handler()
        async def handle_message(message: types.Message):
            response = await self.generate_response(message.text)
            await self.bot.send_message(chat_id=message.chat.id, text=response)

    async def generate_response(self, message):
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=message,
            temperature=0.9,
            max_tokens=1000,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.6,
            stop=["You:"]
        )
        return response['choices'][0]['text']
