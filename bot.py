import logging
import os
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

from handlers import start, show_catalog, show_bot_detail, show_about, error_handler

load_dotenv()
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def main() -> None:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("Falta BOT_TOKEN en el archivo .env")

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("catalogo", show_catalog))

    app.add_handler(CallbackQueryHandler(show_catalog, pattern="^catalog$"))
    app.add_handler(CallbackQueryHandler(show_about, pattern="^about$"))
    app.add_handler(CallbackQueryHandler(show_bot_detail, pattern="^bot_"))

    app.add_error_handler(error_handler)

    logger.info("BotsLab bot iniciado.")
    app.run_polling()


if __name__ == "__main__":
    main()
