from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

class Categories:
    def __init__(self):
        self.menu_keyboard = InlineKeyboardMarkup()
        self.category1 = InlineKeyboardButton('Библиотека', callback_data='category1')
        self.category2 = InlineKeyboardButton('Помощь в выборе языка', callback_data='category2')
        self.category3 = InlineKeyboardButton('Изучение языка программирования', callback_data='category3')
        self.menu_keyboard.add(self.category1, self.category2, self.category3)