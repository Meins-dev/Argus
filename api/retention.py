"""Automatic expiry for hosted conversation and task data."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlalchemy import delete

from .database import SessionLocal
from .models import AnswerCacheEntry, ChatMessage, TaskRecord


def purge_expired_user_data(retention_days: int) -> dict[str, int]:
    if retention_days < 1:
        raise ValueError("retention_days must be at least 1")
    cutoff = datetime.now(timezone.utc) - timedelta(days=retention_days)
    with SessionLocal.begin() as db:
        chat = db.execute(
            delete(ChatMessage).where(ChatMessage.created_at < cutoff)
        ).rowcount or 0
        tasks = db.execute(
            delete(TaskRecord).where(TaskRecord.created_at < cutoff)
        ).rowcount or 0
        cache = db.execute(
            delete(AnswerCacheEntry).where(AnswerCacheEntry.updated_at < cutoff)
        ).rowcount or 0
    return {"chat_messages": chat, "task_records": tasks, "answer_cache_entries": cache}
