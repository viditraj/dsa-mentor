"""Video tutorial search routes."""
from fastapi import APIRouter, Query
from typing import Optional
from video_search import search_videos, get_recommended_videos

router = APIRouter(prefix="/videos", tags=["videos"])


@router.get("/search")
async def search_video_tutorials(
    topic: str = Query(..., description="DSA topic name"),
    problem: Optional[str] = Query(None, description="Specific problem name"),
    q: Optional[str] = Query(None, description="Custom search query override"),
    limit: int = Query(8, ge=1, le=20),
):
    """Search YouTube for DSA tutorial videos related to a topic or problem."""
    return await search_videos(topic=topic, problem=problem, custom_query=q, limit=limit)


@router.get("/recommend/{topic}")
async def get_topic_recommendations(
    topic: str,
    limit: int = Query(5, ge=1, le=10),
):
    """Get curated video recommendations for a topic (multiple search angles)."""
    return await get_recommended_videos(topic=topic, limit=limit)
