from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from keyboard.start_keyboard import start_keyboard

start_router = Router()


@start_router.message(CommandStart())
async def command_start(message: Message) -> None:
    await message.answer(
        f"Привет, абитуриент {hbold(message.from_user.full_name)}",
        reply_markup=start_keyboard()
    )
