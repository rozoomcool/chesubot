import json
from typing import List

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback.get_documents_callback import GetDocumentsCallbackFactory
from callback.get_faculties_callback import GetFacultiesCallbackFactory
from callback.get_faculty_info_callback import GetFacultyInfoCallbackFactory


def faculties_keyboard(data: List[dict]):
    builder = InlineKeyboardBuilder()
    for i, faculty in enumerate(data):
        builder.button(
            text=faculty["faculty"],
            callback_data=GetFacultyInfoCallbackFactory(index=i)
        )
    builder.adjust(2)

    return builder.as_markup()
