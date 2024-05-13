import asyncio
import json
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

import config
from router.documents_router import documents_router
from router.faculties_router import faculties_router
from router.start_router import start_router


async def main() -> None:
    bot = Bot(config.TOKEN, parse_mode=ParseMode.HTML)

    f = open(config.DATA_PATH, "r", encoding="utf_8_sig")
    faculties_data = json.load(f)
    dispatcher = Dispatcher(
        bot=bot,
        faculties_data=faculties_data["faculties"]
    )

    dispatcher.include_router(start_router)
    dispatcher.include_router(faculties_router)
    dispatcher.include_router(documents_router)

    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
