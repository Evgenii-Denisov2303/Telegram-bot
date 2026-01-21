from aiogram.exceptions import TelegramBadRequest


async def send_or_update_hub(
    message,
    text,
    markup,
    ui_state,
    reply_keyboard=None,
    force_new: bool = False
):
    if not force_new:
        message_id = ui_state.get(message.from_user.id)
        if message_id:
            try:
                await message.bot.edit_message_text(
                    text=text,
                    chat_id=message.chat.id,
                    message_id=message_id,
                    reply_markup=markup,
                )
                return
            except:
                pass

    sent = await message.answer(text, reply_markup=markup)
    ui_state[message.from_user.id] = sent.message_id
