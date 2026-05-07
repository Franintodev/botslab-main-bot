from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from bots_catalog import BOTS


def main_menu_keyboard():
    buttons = [
        [InlineKeyboardButton(b["name"], callback_data=f"bot_{b['id']}")]
        for b in BOTS
    ]
    return InlineKeyboardMarkup(buttons)


def bot_detail_keyboard(bot_link: str):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 Abrir bot y suscribirme", url=bot_link)],
        [InlineKeyboardButton("◀️ Ver todos los bots", callback_data="catalog")],
    ])


def back_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("◀️ Ver todos los bots", callback_data="catalog")],
    ])
