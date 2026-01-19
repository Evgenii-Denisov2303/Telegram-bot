from aiogram import Router, F
from aiogram.types import CallbackQuery

from handlers.keyboards import fun_menu_keyboard, zodiac_keyboard
from utils.compliments_blanks import random_compliments, generate_horoscope


router = Router()


@router.callback_query(F.data == "fun:compliment")
async def fun_compliment(call: CallbackQuery):
    await call.message.answer(
        f"💖 {random_compliments()}",
        reply_markup=fun_menu_keyboard(),
    )
    await call.answer()


@router.callback_query(F.data == "fun:game")
async def fun_game(call: CallbackQuery):
    await call.message.answer(
        "🎮 Запускай игру: https://t.me/catizenbot/gameapp?startapp=r_3_2007855",
        reply_markup=fun_menu_keyboard(),
    )
    await call.answer()


@router.callback_query(F.data == "fun:horoscope")
async def fun_horoscope(call: CallbackQuery):
    await call.message.answer(
        "🔮 Выбери знак зодиака:",
        reply_markup=zodiac_keyboard(),
    )
    await call.answer()


@router.callback_query(F.data.startswith("zodiac:"))
async def zodiac_choice(call: CallbackQuery):
    await call.message.answer(
        f"{generate_horoscope()}",
        reply_markup=fun_menu_keyboard(),
    )
    await call.answer()
