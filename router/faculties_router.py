from typing import List

from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hbold, hlink

from callback.get_faculties_callback import GetFacultiesCallbackFactory
from callback.get_faculty_info_callback import GetWayInfoCallbackFactory
from callback.get_ways_callback import GetWaysCallbackFactory
from keyboard.faculties_keyboard import faculty_keyboard, way_keyboard, back_keyboard

faculties_router = Router()


@faculties_router.callback_query(GetFacultiesCallbackFactory.filter())
async def process_get_faculties(callback: CallbackQuery, faculties_data: List[dict]):
    await callback.message.delete()
    await callback.message.answer("Перечень факультетов:\n", reply_markup=faculty_keyboard(faculties_data))


@faculties_router.callback_query(GetWaysCallbackFactory.filter())
async def process_get_ways(callback: CallbackQuery, callback_data: GetWaysCallbackFactory, faculties_data: List[dict]):
    await callback.message.delete()
    await callback.message.answer("Перечень направлений",
                                  reply_markup=way_keyboard(faculties_data, faculty_id=callback_data.facultyId,
                                                            callback_data=callback_data))


@faculties_router.callback_query(GetWayInfoCallbackFactory.filter())
async def process_get_faculties(callback: CallbackQuery, callback_data: GetWayInfoCallbackFactory,
                                faculties_data: List[dict]):
    await callback.message.delete()
    faculty_data = list(filter(lambda x: x["id"] == callback_data.faculty_id, faculties_data))[0]
    way_data = list(filter(lambda x: x["id"] == callback_data.way_id, faculty_data["ways"]))[0]
    text = f"{hlink(title=' ', url=faculty_data["video"])}{hbold(way_data['faculty'])}\n" + way_data["info"]
    await callback.message.answer(text, reply_markup=back_keyboard(GetWaysCallbackFactory(facultyId=callback_data.faculty_id)))
