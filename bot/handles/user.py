from select import select

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.exceptions import MessageNotModified, BadRequest

from bot.handles.states import NameState
from bot.keyboards.keyboards import KeyboardManager
from bot.models.role import UserRole
from bot.services.repository import Repo
from bot.services.tools import create_xlsx, get_file
from models.schemas import User, Role


async def start(m: Message, repo: Repo, db, logger, config, state: FSMContext):
    await state.finish()
    await m.reply(f'Привет, {m.from_user.first_name}')
    await m.bot.send_message(m.chat.id, f'Вы в главном меню', reply_markup=KeyboardManager.start_inline())


async def add_man(cb: CallbackQuery, repo: Repo, db, logger, config, state: FSMContext):
    await cb.bot.send_message(cb.message.chat.id, f'Введите ФИО работника')
    await state.update_data(message_id=cb.message.message_id)
    await NameState.waiting_for_name.set()


async def waiting_name(m: Message, repo: Repo, db, logger, config, state: FSMContext):
    state_data = await state.get_data()
    message_id = state_data['message_id']
    name = m.text
    await m.delete()
    role_id = await repo.get_any_role_id()
    db.add(User(name=name, role_id=role_id))
    db.commit()
    list_users = await repo.list_users_str()
    file = create_xlsx(list_users, message_id)
    f = get_file(file)
    await m.bot.send_document(m.chat.id, f)
    f.close()


def register_user(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'], state='*')

    dp.register_callback_query_handler(add_man, lambda c: c.data == "add_men", state='*')
    dp.register_message_handler(waiting_name, state=NameState.waiting_for_name)
