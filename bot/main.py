import asyncio
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from .config import TELEGRAM_BOT_TOKEN
from bot.handlers.start import start
from bot.handlers.categories import category_callback
from bot.handlers.podcasts import podcast_callback, page_callback, back_to_categories, back_to_podcasts
from bot.handlers.episodes import episode_callback

def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))

    # raw strings avoid the SyntaxWarning
    application.add_handler(CallbackQueryHandler(episode_callback, pattern=r"^ep\|"))
    application.add_handler(CallbackQueryHandler(page_callback, pattern=r"^page\|"))
    application.add_handler(CallbackQueryHandler(podcast_callback, pattern=r"^pod\|"))
    application.add_handler(CallbackQueryHandler(category_callback, pattern=r"^cat\|"))
    application.add_handler(CallbackQueryHandler(back_to_categories, pattern=r"^back_to_categories$"))
    application.add_handler(CallbackQueryHandler(back_to_podcasts, pattern=r"^back_to_podcasts$"))

    print("Bot started. Press Ctrl+C to stop.")
    application.run_polling()

if __name__ == "__main__":
    main()