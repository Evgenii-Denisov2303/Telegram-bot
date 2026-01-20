from aiogram import Router, F
from aiogram.types import CallbackQuery

from handlers.keyboards import action_menu_keyboard


router = Router()


@router.callback_query(F.data == "useful:advice")
async def useful_advice(call: CallbackQuery):
    await call.message.answer(
        "😽 <b>Как гладить котика</b>\n"
        "────────\n"
        "Короткая статья и советы:\n"
        "https://www.feliway.com/ru/Nash-blog/Kak-pravil-no-gladit-koshku/",
        reply_markup=action_menu_keyboard("Еще полезное", "menu:useful"),
    )
    await call.answer()
