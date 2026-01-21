from aiogram.exceptions import TelegramBadRequest


async def send_or_update_hub(message, text, markup, ui_state, reply_keyboard=None):
    chat_id = message.chat.id
    message_id = ui_state.get(message.from_user.id)
    if message_id:
        try:
            await message.bot.edit_message_text(
                text=text,
                chat_id=chat_id,
                message_id=message_id,
                reply_markup=markup,
            )
            return
        except TelegramBadRequest as exc:
            if "message is not modified" in str(exc):
                return

    reply_markup = markup if markup is not None else reply_keyboard
    sent = await message.answer(text, reply_markup=reply_markup)
    ui_state[message.from_user.id] = sent.message_id
