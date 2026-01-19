from aiogram import Router, F
from aiogram.types import CallbackQuery

from handlers.keyboards import useful_menu_keyboard


router = Router()


@router.callback_query(F.data == "useful:advice")
async def useful_advice(call: CallbackQuery):
    await call.message.answer(
        "Советы по уходу за котиками здесь:\n"
        "https://www.feliway.com/ru/Nash-blog/Kak-pravil-no-gladit-koshku/",
        reply_markup=useful_menu_keyboard(),
    )
    await call.answer()
