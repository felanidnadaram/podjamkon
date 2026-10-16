from telegram import Update
from telegram.ext import ContextTypes
from bot.services.db import get_db
from bot.services.podcast_service import get_categories
from bot.keyboards.inline import categories_keyboard

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /start command: show categories."""
    async for session in get_db():
        try:
            categories = await get_categories(session)
            if not categories:
                await update.message.reply_text("No podcast categories available yet.")
                return

            keyboard = categories_keyboard(categories)
            await update.message.reply_text(
                "🎧 *Choose a podcast category:*",
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
        except Exception as e:
            await update.message.reply_text(f"❌ Error loading categories: {e}")