from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def categories_keyboard(categories: list[str]):
    """Build inline keyboard for categories."""
    buttons = [
        [InlineKeyboardButton(category, callback_data=f"cat|{category}")]
        for category in categories
    ]
    return InlineKeyboardMarkup(buttons)

def podcasts_keyboard(podcasts, category: str):
    """Build inline keyboard with podcasts and a back button to categories."""
    buttons = [
        [InlineKeyboardButton(p.title, callback_data=f"pod|{p.id}")]
        for p in podcasts
    ]
    buttons.append([InlineKeyboardButton("« Back to categories", callback_data="back_to_categories")])
    return InlineKeyboardMarkup(buttons)

def episodes_keyboard(episodes, podcast_id: int, page: int, total: int, per_page: int = 10):
    """
    Build inline keyboard for episodes, including pagination if needed.
    Also include a back button to the podcast list.
    """
    buttons = []
    for ep in episodes:
        date_str = ep.publish_date.strftime("%Y-%m-%d") if ep.publish_date else "no date"
        text = f"{ep.title} ({date_str})"
        buttons.append([InlineKeyboardButton(text, callback_data=f"ep|{ep.id}")])

    # Pagination buttons
    total_pages = (total + per_page - 1) // per_page
    nav_buttons = []
    if page > 0:
        nav_buttons.append(
            InlineKeyboardButton("⬅️ Previous", callback_data=f"page|{podcast_id}|{page-1}")
        )
    if page < total_pages - 1:
        nav_buttons.append(
            InlineKeyboardButton("Next ➡️", callback_data=f"page|{podcast_id}|{page+1}")
        )
    if nav_buttons:
        buttons.append(nav_buttons)

    buttons.append([InlineKeyboardButton("« Back to podcasts", callback_data="back_to_podcasts")])
    return InlineKeyboardMarkup(buttons)