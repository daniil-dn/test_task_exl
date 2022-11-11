from aiogram.dispatcher.filters.state import StatesGroup, State


class NameState(StatesGroup):
        waiting_for_name = State()

