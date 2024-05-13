from typing import List

from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hbold

from callback.get_faculties_callback import GetFacultiesCallbackFactory
from callback.get_faculty_info_callback import GetFacultyInfoCallbackFactory
from keyboard.faculties_keyboard import faculties_keyboard

faculties_router = Router()


@faculties_router.callback_query(GetFacultiesCallbackFactory.filter())
async def process_get_faculties(callback: CallbackQuery, faculties_data: List[dict]):
    await callback.message.answer("Перечень направлений:\n", reply_markup=faculties_keyboard(faculties_data))


@faculties_router.callback_query(GetFacultyInfoCallbackFactory.filter())
async def process_get_faculties(callback: CallbackQuery, callback_data: GetFacultyInfoCallbackFactory,
                                faculties_data: List[dict]):
    faculty_data = faculties_data[callback_data.index]
    text = f"{hbold(faculty_data['faculty'])}\n" + faculty_data["info"]
    await callback.message.answer(text)
