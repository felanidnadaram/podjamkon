from telegram import Update
from telegram.ext import ContextTypes
from bot.services.db import get_db
from bot.services.podcast_service import get_podcasts_by_category
from bot.keyboards.inline import podcasts_keyboard

async def category_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle callback when a category is selected."""
    query = update.callback_query
    await query.answer()  # acknowledge

    data = query.data
    if not data.startswith("cat|"):
        return

    category = data.split("|", 1)[1]

    async for session in get_db():
        try:
            podcasts = await get_podcasts_by_category(session, category)
            if not podcasts:
                await query.edit_message_text(
                    f"No podcasts found in category *{category}*.",
                    parse_mode="Markdown"
                )
                return

            keyboard = podcasts_keyboard(podcasts, category)
            await query.edit_message_text(
                f"📚 *{category}* – select a podcast:",
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
        except Exception as e:
            await query.edit_message_text(f"❌ Error: {e}")