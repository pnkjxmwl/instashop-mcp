# src/instashop_mcp/tools/comments.py
import json
from ..clients.instagram_client import InstagramClient


async def get_recent_comments(ig: InstagramClient, media_id: str, limit: int = 50) -> str:

    limit = max(1, min(limit, 100))  # Clamp to valid range

    data = await ig.get(
        f"/{media_id}/comments",
        params={
            "fields": "id,text,timestamp,from,username,parent_id",
            "limit": limit,
        }
    )

    raw_comments = data.get("data", [])

    enriched = []
    for comment in raw_comments:
        sender = comment.get("from", {})
        enriched.append({
            "comment_id": comment["id"],
            "text": comment.get("text", ""),
            "username": sender.get("username") or comment.get("username", "unknown"),
            "author_id": sender.get("id", ""),
            "timestamp": comment.get("timestamp", ""),
            "is_reply": "parent_id" in comment,
        })

    return json.dumps(enriched, ensure_ascii=False, indent=2)


async def reply_to_comment(ig: InstagramClient, comment_id: str, text: str) -> str:

    if not text.strip():
        return json.dumps({"success": False, "error": "Reply text cannot be empty"})

    if len(text) > 2000:
        return json.dumps({
            "success": False,
            "error": f"Reply text is{len(text)} chars; limit is 2000"
        })

    data = await ig.post(
        f"/{comment_id}/replies",
        params={"message": text}
    )

    return json.dumps({
        "success": True,
        "reply_id": data.get("id"),
        "comment_id": comment_id,
        "replied_text": text,
    }, ensure_ascii=False, indent=2)