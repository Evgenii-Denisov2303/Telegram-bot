from aiogram import Router, F
from aiogram.types import CallbackQuery

from handlers.keyboards import zodiac_keyboard, action_menu_keyboard
from utils.compliments_blanks import random_compliments, generate_horoscope


router = Router()


@router.callback_query(F.data == "fun:compliment")
async def fun_compliment(call: CallbackQuery):
    await call.message.answer(
        f"💖 <b>Комплимент</b>\n────────\n{random_compliments()}",
        reply_markup=action_menu_keyboard("Еще комплимент", "fun:compliment"),
    )
    await call.answer()


@router.callback_query(F.data == "fun:game")
async def fun_game(call: CallbackQuery):
    await call.message.answer(
        "🎮 <b>Кошачья игра</b>\n"
        "────────\n"
        "Запускай: https://t.me/catizenbot/gameapp?startapp=r_3_2007855",
        reply_markup=action_menu_keyboard("Еще настроение", "menu:fun"),
    )
    await call.answer()


@router.callback_query(F.data == "fun:horoscope")
async def fun_horoscope(call: CallbackQuery):
    await call.message.answer(
        "🔮 <b>Гороскоп</b>\nВыбери знак зодиака:\n────────",
        reply_markup=zodiac_keyboard(),
    )
    await call.answer()


@router.callback_query(F.data.startswith("zodiac:"))
async def zodiac_choice(call: CallbackQuery):
    await call.message.answer(
        f"🔮 <b>Твой гороскоп</b>\n────────\n{generate_horoscope()}",
        reply_markup=action_menu_keyboard("Еще гороскоп", "fun:horoscope"),
    )
    await call.answer()
