from sqlalchemy import select, func, distinct
from sqlalchemy.ext.asyncio import AsyncSession
from models.podcast import Podcast
from models.episode import Episode

async def get_categories(db: AsyncSession):
    """Return a sorted list of distinct podcast categories."""
    result = await db.execute(select(distinct(Podcast.category)).order_by(Podcast.category))
    return [row[0] for row in result.fetchall()]

async def get_podcasts_by_category(db: AsyncSession, category: str):
    """Return all podcasts belonging to a given category, ordered by title."""
    result = await db.execute(
        select(Podcast).where(Podcast.category == category).order_by(Podcast.title)
    )
    return result.scalars().all()

async def get_podcast_by_id(db: AsyncSession, podcast_id: int):
    """Return a single podcast by its ID or None."""
    result = await db.execute(select(Podcast).where(Podcast.id == podcast_id))
    return result.scalar_one_or_none()

async def get_episodes_page(db: AsyncSession, podcast_id: int, page: int = 0, per_page: int = 10):
    """
    Return a page of episodes for a podcast, ordered by publish_date descending.
    Also return the total number of episodes for pagination calculation.
    """
    # Count total episodes
    count_stmt = select(func.count(Episode.id)).where(Episode.podcast_id == podcast_id)
    total = (await db.execute(count_stmt)).scalar_one()

    # Fetch the requested page
    stmt = (
        select(Episode)
        .where(Episode.podcast_id == podcast_id)
        .order_by(Episode.publish_date.desc())
        .offset(page * per_page)
        .limit(per_page)
    )
    result = await db.execute(stmt)
    episodes = result.scalars().all()
    return episodes, total