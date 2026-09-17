from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterable
from datetime import datetime, timezone

from src.job_agent.sources.models import Job


class JobDatabase:
    """SQLite storage for job listings."""

    def _now_iso(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def __init__(self, database_path: str | Path = "data/jobs.db") -> None:
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._create_table()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _create_table(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS jobs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company_name TEXT NOT NULL,
                    job_title TEXT NOT NULL,
                    job_url TEXT NOT NULL UNIQUE,
                    location TEXT,
                    description TEXT NOT NULL,
                    match_score REAL,
                    match_explanation TEXT,
                    verification_status TEXT DEFAULT 'unverified',
                    generated_cv_filename TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )

    def add_job(self, job: Job | dict[str, str]) -> bool:
        values = job.to_dict() if isinstance(job, Job) else job

        now = self._now_iso()

        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT OR IGNORE INTO jobs
                    (job_title, company_name, location, job_url, description,
                    created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    values["title"],
                    values["company"],
                    values.get("location"),
                    values["url"],
                    values["description"],
                    now,
                    now,
                ),
            )
            return cursor.rowcount == 1
    
    def add_jobs(self, jobs: Iterable[Job | dict[str, str]]) -> int:
        inserted = 0
        now = self._now_iso()

        with self._connect() as connection:
            for job in jobs:
                values = job.to_dict() if isinstance(job, Job) else job

                cursor = connection.execute(
                    """
                    INSERT OR IGNORE INTO jobs
                        (job_title, company_name, location, job_url, description,
                        created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        values["title"],
                        values["company"],
                        values.get("location"),
                        values["url"],
                        values["description"],
                        now,
                        now,
                    ),
                )

                inserted += cursor.rowcount

        return inserted

    def get_jobs(self, limit: int | None = None) -> list[dict[str, str | float | None]]:
        query = "SELECT * FROM jobs ORDER BY id DESC"
        params: tuple = ()

        if limit is not None:
            if limit < 1:
                raise ValueError("limit must be at least 1")
            query += " LIMIT ?"
            params = (limit,)

        with self._connect() as connection:
            rows = connection.execute(query, params).fetchall()
            return [dict(row) for row in rows]

    def update_job_match(
        self,
        job_url: str,
        match_score: float | None,
        match_explanation: str | None,
    ) -> None:
        now = self._now_iso()
        with self._connect() as connection:
            connection.execute(
                """
                UPDATE jobs
                SET match_score = ?,
                    match_explanation = ?,
                    updated_at = ?
                WHERE job_url = ?
                """,
                (match_score, match_explanation, now, job_url),
            )

    def update_job_verification(
        self,
        job_url: str,
        verification_status: str,
    ) -> None:
        now = self._now_iso()
        with self._connect() as connection:
            connection.execute(
                """
                UPDATE jobs
                SET verification_status = ?,
                    updated_at = ?
                WHERE job_url = ?
                """,
                (verification_status, now, job_url),
            )

    def update_job_cv_filename(
        self,
        job_url: str,
        generated_cv_filename: str | None,
    ) -> None:
        now = self._now_iso()
        with self._connect() as connection:
            connection.execute(
                """
                UPDATE jobs
                SET generated_cv_filename = ?,
                    updated_at = ?
                WHERE job_url = ?
                """,
                (generated_cv_filename, now, job_url),
            )