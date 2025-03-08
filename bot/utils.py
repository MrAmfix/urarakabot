from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_inline_keyboard(prefix: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="New picture", callback_data=f"new_picture:{prefix}")]
    ])
    return keyboard
