from aiogram.filters.callback_data import CallbackData


class GetFacultyInfoCallbackFactory(CallbackData, prefix="faculties"):
    index: int
