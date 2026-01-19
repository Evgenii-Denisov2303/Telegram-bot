from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from handlers.keyboards import (
    main_menu_keyboard,
    photos_menu_keyboard,
    fun_menu_keyboard,
    useful_menu_keyboard,
)


router = Router()


WELCOME_TEXT = (
    "🐾 <b>Котик-ботик</b>\n\n"
    "Я умею поднимать настроение фактами, фото и играми. "
    "Выбирай раздел ниже."
)

HELP_TEXT = (
    "📌 <b>Что я умею</b>\n"
    "• фото котиков (включая локальные альбомы)\n"
    "• факты о котах с переводом\n"
    "• гороскоп и комплименты\n"
    "• полезный совет по уходу\n"
    "• опрос и комментарии\n\n"
    "Нажми на нужный раздел в меню."
)


async def _edit_or_send(call: CallbackQuery, text: str, markup):
    try:
        await call.message.edit_text(text, reply_markup=markup)
    except TelegramBadRequest:
        await call.message.answer(text, reply_markup=markup)


@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer(WELCOME_TEXT, reply_markup=main_menu_keyboard())


@router.message(Command("help"))
async def help_command(message: Message):
    await message.answer(HELP_TEXT, reply_markup=main_menu_keyboard())


@router.message()
async def fallback_message(message: Message):
    await message.answer(
        "Не совсем понял сообщение. Выбери раздел из меню.",
        reply_markup=main_menu_keyboard(),
    )


@router.callback_query(F.data == "menu:main")
async def menu_main(call: CallbackQuery):
    await _edit_or_send(call, WELCOME_TEXT, main_menu_keyboard())
    await call.answer()


@router.callback_query(F.data == "menu:help")
async def menu_help(call: CallbackQuery):
    await _edit_or_send(call, HELP_TEXT, main_menu_keyboard())
    await call.answer()


@router.callback_query(F.data == "menu:photos")
async def menu_photos(call: CallbackQuery):
    await _edit_or_send(
        call,
        "📸 Выбери котика или попроси случайное фото.",
        photos_menu_keyboard(),
    )
    await call.answer()


@router.callback_query(F.data == "menu:fun")
async def menu_fun(call: CallbackQuery):
    await _edit_or_send(
        call,
        "✨ Небольшая порция настроения на выбор.",
        fun_menu_keyboard(),
    )
    await call.answer()


@router.callback_query(F.data == "menu:useful")
async def menu_useful(call: CallbackQuery):
    await _edit_or_send(
        call,
        "🧼 Полезный раздел про уход.",
        useful_menu_keyboard(),
    )
    await call.answer()
