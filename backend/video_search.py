"""YouTube video search service for DSA tutorials."""
import asyncio
from typing import Optional
from youtubesearchpython import VideosSearch

# Curated DSA channels for quality filtering / boosting
TRUSTED_DSA_CHANNELS = {
    "NeetCode", "NeetCodeIO",
    "Abdul Bari",
    "mycodeschool",
    "Back To Back SWE",
    "Tushar Roy - Coding Made Simple",
    "William Fiset",
    "Errichto",
    "Kevin Naughton Jr.",
    "Nick White",
    "take U forward",
    "Striver",
    "CodeWithHarry",
    "freeCodeCamp.org",
    "CS Dojo",
    "Reducible",
    "3Blue1Brown",
    "Jenny's Lectures CS IT",
    "Apna College",
    "Kunal Kushwaha",
    "Tech With Tim",
    "Fireship",
    "HackerRank",
    "LeetCode",
    "GeeksforGeeks",
    "Programiz",
    "Gate Smashers",
}

# Topic -> best search queries for high-quality results
TOPIC_SEARCH_HINTS = {
    "Big-O Notation & Complexity Analysis": "big O notation time complexity explained",
    "Arrays & Strings": "arrays data structure tutorial",
    "Hash Tables & Sets": "hash table tutorial how it works",
    "Two Pointers": "two pointer technique leetcode",
    "Sliding Window": "sliding window algorithm tutorial",
    "Linked Lists": "linked list data structure tutorial",
    "Stacks": "stack data structure tutorial",
    "Queues & Deques": "queue deque data structure tutorial",
    "Binary Search": "binary search algorithm tutorial",
    "Recursion & Backtracking": "recursion backtracking tutorial",
    "Binary Trees": "binary tree tutorial",
    "Binary Search Trees": "BST binary search tree tutorial",
    "Heaps & Priority Queues": "heap priority queue tutorial",
    "Tries": "trie data structure tutorial",
    "Graphs - BFS & DFS": "graph BFS DFS traversal tutorial",
    "Graphs - Shortest Path": "dijkstra shortest path algorithm",
    "Graphs - Advanced": "topological sort minimum spanning tree",
    "Dynamic Programming - 1D": "dynamic programming tutorial beginners",
    "Dynamic Programming - 2D": "2D dynamic programming tutorial",
    "Greedy Algorithms": "greedy algorithm tutorial",
    "Intervals": "interval problems merge intervals",
    "Sorting Algorithms": "sorting algorithms explained",
    "Bit Manipulation": "bit manipulation tutorial programming",
    "Math & Geometry": "math algorithms programming",
    "Union Find": "union find disjoint set tutorial",
    "Segment Trees & BIT": "segment tree tutorial",
    "Advanced Patterns": "monotonic stack sliding window maximum",
}


def _build_search_query(topic: str, problem: Optional[str] = None, custom_query: Optional[str] = None) -> str:
    """Build an optimized YouTube search query."""
    if custom_query:
        return custom_query

    if problem:
        return f"{problem} leetcode solution explanation"

    # Use hint if available, else construct from topic name
    if topic in TOPIC_SEARCH_HINTS:
        return TOPIC_SEARCH_HINTS[topic]

    return f"{topic} data structure algorithm tutorial"


def _score_video(video: dict) -> float:
    """Score a video for relevance and quality."""
    score = 0.0
    channel = video.get("channel", {}).get("name", "")
    title = (video.get("title") or "").lower()
    views = video.get("viewCount", {})
    duration = video.get("duration", "")

    # Trusted channel bonus
    if channel in TRUSTED_DSA_CHANNELS:
        score += 30

    # View count signal
    view_text = views.get("text", "0") if isinstance(views, dict) else str(views)
    view_num = _parse_view_count(view_text)
    if view_num > 1_000_000:
        score += 20
    elif view_num > 100_000:
        score += 12
    elif view_num > 10_000:
        score += 5

    # Duration preference (5-30 min is ideal for tutorials)
    minutes = _parse_duration_minutes(duration)
    if 5 <= minutes <= 30:
        score += 10
    elif 30 < minutes <= 60:
        score += 5
    elif minutes > 60:
        score += 2  # full courses still okay

    # Title quality signals
    positive = ["tutorial", "explained", "solution", "how to", "learn", "guide", "walkthrough", "step by step"]
    negative = ["shorts", "#shorts", "tiktok", "meme", "funny", "reaction"]
    for p in positive:
        if p in title:
            score += 3
    for n in negative:
        if n in title:
            score -= 15

    return score


def _parse_view_count(text: str) -> int:
    """Parse '1,234,567 views' or '1.2M views' into int."""
    text = text.lower().replace(",", "").replace("views", "").strip()
    try:
        if "m" in text:
            return int(float(text.replace("m", "").strip()) * 1_000_000)
        elif "k" in text:
            return int(float(text.replace("k", "").strip()) * 1_000)
        elif "b" in text:
            return int(float(text.replace("b", "").strip()) * 1_000_000_000)
        return int(text) if text else 0
    except (ValueError, TypeError):
        return 0


def _parse_duration_minutes(duration: str) -> float:
    """Parse '12:34' or '1:02:34' into minutes."""
    if not duration:
        return 0
    parts = duration.split(":")
    try:
        if len(parts) == 3:
            return int(parts[0]) * 60 + int(parts[1]) + int(parts[2]) / 60
        elif len(parts) == 2:
            return int(parts[0]) + int(parts[1]) / 60
        return 0
    except (ValueError, TypeError):
        return 0


def _format_video(video: dict) -> dict:
    """Format a video result for API response."""
    vid_id = video.get("id", "")
    channel = video.get("channel", {})
    thumbnails = video.get("thumbnails", [])
    views = video.get("viewCount", {})
    view_text = views.get("short", views.get("text", "")) if isinstance(views, dict) else str(views)

    return {
        "id": vid_id,
        "title": video.get("title", ""),
        "url": f"https://www.youtube.com/watch?v={vid_id}",
        "embed_url": f"https://www.youtube.com/embed/{vid_id}",
        "thumbnail": thumbnails[-1]["url"] if thumbnails else None,
        "duration": video.get("duration", ""),
        "channel": channel.get("name", "") if isinstance(channel, dict) else str(channel),
        "channel_url": channel.get("link", "") if isinstance(channel, dict) else "",
        "views": view_text,
        "published": video.get("publishedTime", ""),
        "description_snippet": (video.get("descriptionSnippet") or [{}])[0].get("text", "") if video.get("descriptionSnippet") else "",
        "is_trusted_channel": (channel.get("name", "") if isinstance(channel, dict) else "") in TRUSTED_DSA_CHANNELS,
    }


async def search_videos(
    topic: str,
    problem: Optional[str] = None,
    custom_query: Optional[str] = None,
    limit: int = 8,
) -> dict:
    """Search YouTube for DSA tutorial videos, ranked by quality."""
    query = _build_search_query(topic, problem, custom_query)

    # Run the sync YouTube search in a thread pool
    def _search():
        vs = VideosSearch(query, limit=min(limit * 2, 20))  # fetch more for ranking
        return vs.result()

    result = await asyncio.to_thread(_search)
    videos = result.get("result", [])

    # Score and rank
    scored = [(v, _score_video(v)) for v in videos]
    scored.sort(key=lambda x: x[1], reverse=True)

    formatted = [_format_video(v) for v, _ in scored[:limit]]

    return {
        "query": query,
        "topic": topic,
        "problem": problem,
        "videos": formatted,
        "total_found": len(videos),
        "best_pick": formatted[0] if formatted else None,
    }


async def get_recommended_videos(topic: str, limit: int = 5) -> dict:
    """Get curated recommendations for a topic with multiple search angles."""
    queries = []

    # Main concept query
    if topic in TOPIC_SEARCH_HINTS:
        queries.append(TOPIC_SEARCH_HINTS[topic])
    else:
        queries.append(f"{topic} tutorial")

    # Add a "visualized / animated" query for concepts
    queries.append(f"{topic} algorithm visualization animated")

    # Run searches concurrently
    tasks = [asyncio.to_thread(lambda q=q: VideosSearch(q, limit=5).result()) for q in queries]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    all_videos = []
    seen_ids = set()
    for r in results:
        if isinstance(r, Exception):
            continue
        for v in r.get("result", []):
            if v.get("id") not in seen_ids:
                seen_ids.add(v.get("id"))
                all_videos.append(v)

    # Score and deduplicate
    scored = [(v, _score_video(v)) for v in all_videos]
    scored.sort(key=lambda x: x[1], reverse=True)

    formatted = [_format_video(v) for v, _ in scored[:limit]]

    return {
        "topic": topic,
        "videos": formatted,
        "best_pick": formatted[0] if formatted else None,
    }
