# CHESU bot
### Телеграмм бот для абитуриентов, которые хотят ознакомиться с университетом.

#### Использованные технологии
  - aiogram - Библиотека, для создания телеграмм ботов
  - python-dotenv - Библиотека, для управления переменными окружения

#### Функционал
  - Приветствие пользователя с кнопками для ознакомления с факультетами и направлениями
  - Просмотр перечня документов для поступления в университет
  - Просмотр факультетов, которые есть в университете
  - Просмотр направлений, которые есть в факультетах
  - Вывод информации о направлении с видео-аннотацией о каждом факультете

#### Структура проекта
  - main.py - Главный файл, в нем функционал запуска бота, настройки всех зависимостей и роутеров
  - config.py - Подгружает все значения из environment
  - Dockerfile - Файл для настройки docker, для удобного запуска и обслуживания бота на сервере
  - requirements.txt - Содержит перечень библиотек, для удобства управления ими
  - .env - настройка переменных окружения
  - /callback - Содержит коллбэки, которые преднозначены для вызова функций из бота
  - /keyboard - Настройка клавиатур, которые будут в боте
  - /resourse - Содержит data.json, который выполняет роль базы данных
  - /router - Настройка роутеров в боте
  - /utils - Вспомогательный функционал

#### Ключевые моменты
  - Инициализация бота: `bot = Bot(config.TOKEN, parse_mode=ParseMode.HTML)`
  - Подгрузка данных из data.json:
```
f = open(config.DATA_PATH, "r", encoding="utf_8_sig")
faculties_data = json.load(f)
```
  - Инъкция зависимостей, для избежания использования глобальных переменных и улучшения читаемости кода
```
dispatcher = Dispatcher(
    bot=bot,
    faculties_data=faculties_data["faculties"]
)
```
  - Добавление роутеров
```
dispatcher.include_router(start_router)
dispatcher.include_router(faculties_router)
dispatcher.include_router(documents_router)
```
  - Запуск поллинга бота: `await dispatcher.start_polling(bot)`
  - Настройка логирования и запуск бота в асинхронном режиме
```
if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO, stream=sys.stdout)
  asyncio.run(main())
```
  - Коллбэки, которые служат для вызова функций и передачи между ними параметров
```
class GetDocumentsCallbackFactory(CallbackData, prefix="documents"):
    pass
class GetFacultiesCallbackFactory(CallbackData, prefix="faculties"):
    pass
class GetWayInfoCallbackFactory(CallbackData, prefix="faculties"):
    faculty_id: int
    way_id: int
class GetWaysCallbackFactory(CallbackData, prefix="ways"):
    facultyId: int
class StartCallback(CallbackData, prefix="startt"):
    pass
```

#### Стартовый роутер
##### Инизиализация роутера: `start_router = Router()`
##### Ендпоинт для команды /start
```
@start_router.message(CommandStart())
async def command_start(message: Message) -> None:
    await message.answer(
        f"Привет, абитуриент {hbold(message.from_user.full_name)}",
        reply_markup=start_keyboard()
    )
```
##### Коллбэк, который вызывает фукнцию start
```
@start_router.callback_query(StartCallback.filter())
async def command_start(callback: CallbackQuery) -> None:
    await callback.message.delete()
    await callback.message.answer(
        f"Привет, абитуриент {hbold(callback.from_user.full_name)}",
        reply_markup=start_keyboard()
    )
```

#### Роутер с информацией о документах
##### Инизиализация роутера: `documents_router = Router()`
##### Коллбэк для выдачи перечня документов
```
@documents_router.callback_query(GetDocumentsCallbackFactory.filter())
async def process_get_documents(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(texts.documents_info, reply_markup=document_keyboard())
```

#### Роутер с информацией о факультетах и направлениях
##### Инизиализация роутера: `faculties_router = Router()`
##### Коллбэк получения списка факультетов
```
@start_router.message(CommandStart())
@faculties_router.callback_query(GetFacultiesCallbackFactory.filter())
async def process_get_faculties(callback: CallbackQuery, faculties_data: List[dict]):
    await callback.message.delete()
    await callback.message.answer("Перечень факультетов:\n", reply_markup=faculty_keyboard(faculties_data))

```
##### Коллбэк для получния списка направлений
```
@faculties_router.callback_query(GetWaysCallbackFactory.filter())
async def process_get_ways(callback: CallbackQuery, callback_data: GetWaysCallbackFactory, faculties_data: List[dict]):
    await callback.message.delete()
    await callback.message.answer("Перечень направлений",
                                  reply_markup=way_keyboard(faculties_data, faculty_id=callback_data.facultyId,
                                  callback_data=callback_data))

```
##### Коллбэк для получения информации о направлении, с видеоанонсом
```
@faculties_router.callback_query(GetWayInfoCallbackFactory.filter())
async def process_get_faculties(callback: CallbackQuery, callback_data: GetWayInfoCallbackFactory,
                                faculties_data: List[dict]):
    await callback.message.delete()
    faculty_data = list(filter(lambda x: x["id"] == callback_data.faculty_id, faculties_data))[0]
    way_data = list(filter(lambda x: x["id"] == callback_data.way_id, faculty_data["ways"]))[0]
    text = f"{hlink(title=' ', url=faculty_data["video"])}{hbold(way_data['faculty'])}\n" + way_data["info"]
    await callback.message.answer(text, reply_markup=back_keyboard(GetWaysCallbackFactory(facultyId=callback_data.faculty_id)))
```

#### Настройка клавиатур в боте
```
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
```







