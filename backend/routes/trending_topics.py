"""Trending Tech Topics API routes — web-sourced, interview-focused."""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from agents import fetch_trending_topics, deep_dive_topic

router = APIRouter()


@router.get("/")
async def get_trending_topics(category: str = "all"):
    """Fetch trending tech topics from HN + dev.to, filtered for interview relevance."""
    return await fetch_trending_topics(category=category)


class DeepDiveRequest(BaseModel):
    topic_title: str
    topic_context: Optional[str] = ""


@router.post("/deep-dive")
async def get_deep_dive(req: DeepDiveRequest):
    """Generate an in-depth interview-ready explanation of a specific topic."""
    return await deep_dive_topic(
        topic_title=req.topic_title,
        topic_context=req.topic_context or "",
    )
