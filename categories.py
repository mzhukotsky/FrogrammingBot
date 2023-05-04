from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
class Categories:
    def __init__(self):
        pass

    def menu_keyboard_with_subcategories(self):
        # Create inline keyboard
        keyboard = InlineKeyboardMarkup()
        button_library = InlineKeyboardButton("Библиотека", callback_data='category_library')
        button_roadmaps = InlineKeyboardButton("Помощь в выборе языка", callback_data='category_roadmaps')
        button_chat = InlineKeyboardButton("Изучение языка", callback_data='category_chat')
        keyboard.add(button_library, button_roadmaps, button_chat)

        return keyboard
        
    def login_button_keyboard(self):
        login_button = KeyboardButton('Войти')
        reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        reply_keyboard.add(login_button)
        
        # Return both keyboards as a tuple
        return reply_keyboard