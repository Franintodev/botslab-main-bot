import logging
from telegram import Update
from telegram.ext import ContextTypes
from bots_catalog import BOTS
from keyboards import main_menu_keyboard, bot_detail_keyboard, back_keyboard

logger = logging.getLogger(__name__)

WELCOME_TEXT = (
    "👋 ¡Hola, {first_name}! Bienvenido a <b>BotsLab</b>.\n\n"
    "<i>Tu productividad, automatizada. Sin costos de más.</i>\n\n"
    "Aquí encuentras todos nuestros bots. Selecciona uno para "
    "conocer más y suscribirte:"
)

ABOUT_TEXT = (
    "🤖 *¿Qué es BotsLab?*\n\n"
    "Somos un equipo que construye bots de Telegram para hacer tu "
    "día a día más fácil y productivo.\n\n"
    "Cada bot está diseñado para resolver un problema real, sin complicaciones "
    "y al menor costo posible.\n\n"
    "💬 ¿Tienes alguna idea o necesitas algo personalizado? "
    "Escríbenos a @BotsLabSoporte."
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    first_name = update.effective_user.first_name or "amigo"
    await update.message.reply_text(
        WELCOME_TEXT.format(first_name=first_name),
        parse_mode="HTML",
        reply_markup=main_menu_keyboard(),
    )


async def show_catalog(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "🛒 <b>Catálogo de bots BotsLab</b>\n\nSelecciona un bot para ver más detalles:",
        parse_mode="HTML",
        reply_markup=main_menu_keyboard(),
    )


async def show_bot_detail(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    bot_id = query.data.replace("bot_", "")
    bot = next((b for b in BOTS if b["id"] == bot_id), None)

    if not bot:
        await query.edit_message_text("❌ Bot no encontrado.", reply_markup=back_keyboard())
        return

    text = f"{bot['description']}\n\n💳 <b>Precio:</b> {bot['price']}"
    await query.edit_message_text(
        text,
        parse_mode="HTML",
        reply_markup=bot_detail_keyboard(bot["link"]),
    )


async def show_about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        ABOUT_TEXT,
        parse_mode="HTML",
        reply_markup=back_keyboard(),
    )


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Error en el bot:", exc_info=context.error)
    if update and hasattr(update, "callback_query") and update.callback_query:
        await update.callback_query.answer("⚠️ Ocurrió un error, intentá de nuevo.")
