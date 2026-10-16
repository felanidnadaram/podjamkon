from telegram import Update
from telegram.ext import ContextTypes
from sqlalchemy import select
from models.episode import Episode
from bot.services.db import get_db
from bot.services.s3_service import generate_download_url

async def episode_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle episode selection – send a signed download link."""
    query = update.callback_query
    await query.answer()

    data = query.data
    if not data.startswith("ep|"):
        return

    episode_id = int(data.split("|")[1])

    async for session in get_db():
        try:
            result = await session.execute(select(Episode).where(Episode.id == episode_id))
            episode = result.scalar_one_or_none()
            if not episode:
                await query.answer("Episode not found.", show_alert=True)
                return

            # Generate signed URL
            signed_url = generate_download_url(episode.file_key)

            # Send download link as a new message (not editing the list)
            await query.message.reply_text(
                f"🎧 *{episode.title}*\n\n"
                f"⬇️ [Download link]({signed_url})\n"
                f"_(valid for 10 minutes)_",
                parse_mode="Markdown",
                disable_web_page_preview=True
            )
        except Exception as e:
            await query.message.reply_text(f"❌ Failed to generate download link: {e}")