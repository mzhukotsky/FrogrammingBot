from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

class RoadmapSelection:
    def __init__(self):
        self.menu_keyboard = InlineKeyboardMarkup()
        self.roadmaps = ['Python', 'Java', 'JavaScript']

        # Создаем кнопки для каждого языка
        for maps in self.roadmaps:
            button = InlineKeyboardButton(maps, callback_data=f'language_{maps}')
            self.menu_keyboard.add(button)