import json
from typing import List

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback.get_documents_callback import GetDocumentsCallbackFactory
from callback.get_faculties_callback import GetFacultiesCallbackFactory
from callback.get_faculty_info_callback import GetWayInfoCallbackFactory
from callback.get_ways_callback import GetWaysCallbackFactory
from callback.start_callback import StartCallback


def faculty_keyboard(data: List[dict]):
    builder = InlineKeyboardBuilder()
    for i, faculty in enumerate(data):
        builder.button(
            text=faculty["name"],
            callback_data=GetWaysCallbackFactory(facultyId=int(faculty["id"]))
        )
    builder.adjust(2)
    builder.button(
        text="🔙 Назад",
        callback_data=StartCallback()
    )
    builder.adjust(1)

    return builder.as_markup()


def document_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🔙 Назад",
        callback_data=StartCallback()
    )
    builder.adjust(1)

    return builder.as_markup()


def back_keyboard(callback_data):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🔙 Назад",
        callback_data=callback_data
    )
    builder.adjust(1)

    return builder.as_markup()


def way_keyboard(data: List[dict], faculty_id: int, callback_data):
    builder = InlineKeyboardBuilder()
    for i, faculty in enumerate(list(filter(lambda d: d["id"] == faculty_id, data))[0]["ways"]):
        builder.button(
            text=faculty["faculty"],
            callback_data=GetWayInfoCallbackFactory(way_id=faculty["id"], faculty_id=faculty_id)
        )
    builder.adjust(2)
    builder.button(
        text="🔙 Назад",
        callback_data=GetFacultiesCallbackFactory()
    )

    return builder.as_markup()
