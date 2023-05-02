from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class Categories:
    def __init__(self):
        pass

    def menu_keyboard_with_subcategories(self):
        keyboard = InlineKeyboardMarkup()
        button_library = InlineKeyboardButton("Библиотека", callback_data='category_library')
        button_roadmaps = InlineKeyboardButton("Помощь в выборе языка", callback_data='category_roadmaps')
        button_chat = InlineKeyboardButton("Изучение языка", callback_data='category_chat')
        keyboard.add(button_library, button_roadmaps, button_chat)
        return keyboard