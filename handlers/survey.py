import asyncio

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from handlers.keyboards import survey_keyboard, main_menu_keyboard


router = Router()


class CommentState(StatesGroup):
    waiting_for_comment = State()


@router.message(Command("survey"))
async def survey_command(message: Message):
    await message.answer(
        "⭐ Оцени бота или оставь комментарий.",
        reply_markup=survey_keyboard(),
    )


@router.callback_query(F.data == "survey:open")
async def survey_open(call: CallbackQuery):
    await call.message.answer(
        "⭐ Оцени бота или оставь комментарий.",
        reply_markup=survey_keyboard(),
    )
    await call.answer()


@router.callback_query(F.data == "survey:rate")
async def survey_rate(call: CallbackQuery):
    await call.message.answer_poll(
        question="Как тебе бот?",
        options=["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"],
        is_anonymous=False,
        allows_multiple_answers=False,
    )
    await call.answer()


@router.callback_query(F.data == "survey:comment")
async def survey_comment(call: CallbackQuery, state: FSMContext):
    await state.set_state(CommentState.waiting_for_comment)
    await call.message.answer("💬 Напиши комментарий одним сообщением.")
    await call.answer()


@router.message(CommentState.waiting_for_comment)
async def handle_comment(message: Message, state: FSMContext):
    comment = message.text.strip() if message.text else ""
    if not comment:
        await message.answer("Похоже, комментарий пустой. Попробуй еще раз.")
        return

    await asyncio.to_thread(_append_comment, message.from_user.id, comment)
    await state.clear()
    await message.answer(
        "Спасибо за отзыв! 😊",
        reply_markup=main_menu_keyboard(),
    )


def _append_comment(user_id: int, comment: str) -> None:
    with open("comments.txt", "a", encoding="utf-8") as file:
        file.write(f"User {user_id}: {comment}\n")
