from aiogram.filters.callback_data import CallbackData


class GetWayInfoCallbackFactory(CallbackData, prefix="faculties"):
    faculty_id: int
    way_id: int
