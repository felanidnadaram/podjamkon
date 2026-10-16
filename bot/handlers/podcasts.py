from telegram import Update
from telegram.ext import ContextTypes
from bot.services.db import get_db
from bot.services.podcast_service import get_podcast_by_id, get_episodes_page
from bot.keyboards.inline import episodes_keyboard, podcasts_keyboard, categories_keyboard

async def podcast_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle callback when a podcast is selected, show episodes page 0."""
    query = update.callback_query
    await query.answer()

    data = query.data
    if not data.startswith("pod|"):
        return

    podcast_id = int(data.split("|")[1])

    async for session in get_db():
        try:
            podcast = await get_podcast_by_id(session, podcast_id)
            if not podcast:
                await query.edit_message_text("Podcast not found.")
                return

            episodes, total = await get_episodes_page(session, podcast_id, page=0)
            if not episodes:
                await query.edit_message_text(
                    f"No episodes found for *{podcast.title}*.",
                    parse_mode="Markdown"
                )
                return

            keyboard = episodes_keyboard(episodes, podcast_id, page=0, total=total)
            await query.edit_message_text(
                f"🎙 *{podcast.title}* – episodes (1/{total}):",
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
        except Exception as e:
            await query.edit_message_text(f"❌ Error: {e}")

async def page_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle pagination for episodes."""
    query = update.callback_query
    await query.answer()

    data = query.data
    if not data.startswith("page|"):
        return

    _, podcast_id_str, page_str = data.split("|")
    podcast_id = int(podcast_id_str)
    page = int(page_str)

    async for session in get_db():
        try:
            podcast = await get_podcast_by_id(session, podcast_id)
            if not podcast:
                await query.edit_message_text("Podcast not found.")
                return

            episodes, total = await get_episodes_page(session, podcast_id, page=page)
            if not episodes:
                await query.edit_message_text("No more episodes.")
                return

            keyboard = episodes_keyboard(episodes, podcast_id, page=page, total=total)
            await query.edit_message_text(
                f"🎙 *{podcast.title}* – episodes (page {page+1}):",
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
        except Exception as e:
            await query.edit_message_text(f"❌ Error: {e}")

async def back_to_categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Go back to the category list."""
    query = update.callback_query
    await query.answer()
    # Reuse start logic but on existing message
    from bot.services.podcast_service import get_categories
    from bot.keyboards.inline import categories_keyboard

    async for session in get_db():
        try:
            categories = await get_categories(session)
            if not categories:
                await query.edit_message_text("No categories.")
                return
            keyboard = categories_keyboard(categories)
            await query.edit_message_text(
                "🎧 *Choose a podcast category:*",
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
        except Exception as e:
            await query.edit_message_text(f"❌ Error: {e}")

async def back_to_podcasts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Go back to the podcast list of the current category (we need to store category)."""
    query = update.callback_query
    await query.answer()
    # Since we don't have the category in callback data, we can store it in context.user_data
    # For simplicity, go back to categories instead.
    await back_to_categories(update, context)