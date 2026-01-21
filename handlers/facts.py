import asyncio
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from database.db_setup import get_user_facts, update_user_facts
from handlers.keyboards import facts_nav_keyboard
from handlers.ui import send_or_update_hub
from services.cat_fact_api import fetch_cat_fact
from services.translate_api import translate_text
from utils.concurrency import acquire_or_notify


router = Router()

MAX_FACTS_PER_USER = 80

FACTS_HUB_TEXT = (
    "📚 <b>Факты</b>\n"
    "Нажимай «Новый», чтобы получать факты.\n"
    "────────"
)


# ---------- helpers ----------

def _format_fact(original: str, translation: str | None) -> str:
    if not translation:
        return (
            "🧠 <b>Кошачий факт</b>\n"
            "────────\n"
            f"🇬🇧 {original}\n\n"
            "❌ Перевод недоступен"
        )
    return (
        "🧠 <b>Кошачий факт</b>\n"
        "────────\n"
        f"🇬🇧 {original}\n\n"
        f"🇷🇺 {translation}"
    )


async def _send_fact_and_menu(
    message: Message,
    facts: list,
    index: int,
    ui_state,
):
    fact_data = facts[index]
    text = fact_data["display_text"]

    # 1) факт — новым сообщением (внизу)
    await message.answer(text)

    # 2) хаб/меню фактов — тоже вниз
    await send_or_update_hub(
        message,
        FACTS_HUB_TEXT,
        facts_nav_keyboard(
            has_prev=index > 0,
            has_next=index < len(facts) - 1,
        ),
        ui_state,
        repost=True,
    )


# ---------- menu entry ----------

@router.callback_query(F.data == "menu:facts")
async def menu_facts(
    call: CallbackQuery,
    session,
    settings,
    cache,
    semaphore,
    ui_state,
):
    if not await acquire_or_notify(semaphore, call):
        return

    try:
        fact = await fetch_cat_fact(session, settings, cache)
        if not fact:
            await call.answer("Не удалось получить факт.", show_alert=True)
            return

        translation = await translate_text(session, settings, cache, fact)

    finally:
        semaphore.release()

    display_text = _format_fact(fact, translation)

    data = await get_user_facts(call.from_user.id)
    facts = data["facts"]

    facts.append(
        {
            "text": fact,
            "translation": translation,
            "display_text": display_text,
        }
    )

    if len(facts) > MAX_FACTS_PER_USER:
        facts = facts[-MAX_FACTS_PER_USER :]

    index = len(facts) - 1

    await update_user_facts(call.from_user.id, facts, index)
    await _send_fact_and_menu(call.message, facts, index, ui_state)
    await call.answer()


# ---------- reply keyboard entry ----------

@router.message(F.text == "Факты")
async def menu_facts_message(
    message: Message,
    session,
    settings,
    cache,
    semaphore,
    ui_state,
):
    try:
        await asyncio.wait_for(semaphore.acquire(), timeout=0.2)
    except asyncio.TimeoutError:
        await message.answer("Я чуть занят 😺 Попробуй снова.")
        return

    try:
        fact = await fetch_cat_fact(session, settings, cache)
        if not fact:
            await message.answer("Не удалось получить факт.")
            return

        translation = await translate_text(session, settings, cache, fact)

    finally:
        semaphore.release()

    display_text = _format_fact(fact, translation)

    data = await get_user_facts(message.from_user.id)
    facts = data["facts"]

    facts.append(
        {
            "text": fact,
            "translation": translation,
            "display_text": display_text,
        }
    )

    if len(facts) > MAX_FACTS_PER_USER:
        facts = facts[-MAX_FACTS_PER_USER :]

    index = len(facts) - 1

    await update_user_facts(message.from_user.id, facts, index)
    await _send_fact_and_menu(message, facts, index, ui_state)


# ---------- navigation ----------

@router.callback_query(F.data.in_({"facts:new", "facts:prev", "facts:next"}))
async def facts_nav(
    call: CallbackQuery,
    session,
    settings,
    cache,
    semaphore,
    ui_state,
):
    data = await get_user_facts(call.from_user.id)
    facts = data["facts"]
    index = data["current_index"]

    if call.data == "facts:new":
        if not await acquire_or_notify(semaphore, call):
            return

        try:
            fact = await fetch_cat_fact(session, settings, cache)
            if not fact:
                await call.answer("Не удалось получить факт.", show_alert=True)
                return

            translation = await translate_text(session, settings, cache, fact)

        finally:
            semaphore.release()

        display_text = _format_fact(fact, translation)

        facts.append(
            {
                "text": fact,
                "translation": translation,
                "display_text": display_text,
            }
        )

        if len(facts) > MAX_FACTS_PER_USER:
            facts = facts[-MAX_FACTS_PER_USER :]

        index = len(facts) - 1

    elif call.data == "facts:prev" and index > 0:
        index -= 1

    elif call.data == "facts:next" and index < len(facts) - 1:
        index += 1

    if not facts:
        await call.message.answer("Фактов пока нет. Нажми «Новый».")
        await call.answer()
        return

    await update_user_facts(call.from_user.id, facts, index)
    await _send_fact_and_menu(call.message, facts, index, ui_state)
    await call.answer()