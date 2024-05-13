from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback.get_documents_callback import GetDocumentsCallbackFactory
from callback.get_faculties_callback import GetFacultiesCallbackFactory


def start_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Выбрать институт",
        callback_data=GetFacultiesCallbackFactory()
    )
    builder.button(
        text="Документы для поступления",
        callback_data=GetDocumentsCallbackFactory()
    )
    builder.adjust(2)

    return builder.as_markup()
