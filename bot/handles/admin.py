from aiogram import Dispatcher, types
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageNotModified, BadRequest

from bot.models.role import UserRole
from bot.services.repository import Repo
from bot.keyboards.keyboards import KeyboardManager


async def admin_command(m: Message, repo: Repo, db, logger, config, state):
    await state.reset_data()
    await m.reply(f'✌️Привет, {m.from_user.first_name} ✌️')
    return




def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_command, commands=['admin'], state='*', role=UserRole.ADMIN)
