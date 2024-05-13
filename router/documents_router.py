from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hbold

from callback.get_documents_callback import GetDocumentsCallbackFactory
from keyboard.faculties_keyboard import document_keyboard
from utils import texts

documents_router = Router()


@documents_router.callback_query(GetDocumentsCallbackFactory.filter())
async def process_get_documents(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(texts.documents_info, reply_markup=document_keyboard())
