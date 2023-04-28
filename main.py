import asyncio
from telegram_bot import TelegramBot

loop = asyncio.get_event_loop()
bot = TelegramBot(loop=loop)
bot.start()

try:
    loop.run_forever()
finally:
    loop.close()