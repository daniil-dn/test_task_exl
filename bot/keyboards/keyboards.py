from aiogram import types


class KeyboardManager:
    @staticmethod
    def start_inline():
        kb = types.InlineKeyboardMarkup(row_width=1)
        kb.add(types.InlineKeyboardButton('Записать работника', callback_data='add_men'))
        return kb
