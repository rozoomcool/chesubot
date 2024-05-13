from aiogram.filters.callback_data import CallbackData


class GetWaysCallbackFactory(CallbackData, prefix="ways"):
    facultyId: int
