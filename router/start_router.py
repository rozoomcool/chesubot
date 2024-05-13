from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold

from callback.start_callback import StartCallback
from keyboard.start_keyboard import start_keyboard

start_router = Router()


@start_router.message(CommandStart())
async def command_start(message: Message) -> None:
    await message.answer(
        f"Привет, абитуриент {hbold(message.from_user.full_name)}",
        reply_markup=start_keyboard()
    )


@start_router.callback_query(StartCallback.filter())
async def command_start(callback: CallbackQuery) -> None:
    await callback.message.delete()
    await callback.message.answer(
        f"Привет, абитуриент {hbold(callback.from_user.full_name)}",
        reply_markup=start_keyboard()
    )
