from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterable

from src.job_agent.sources.models import Job


class JobDatabase:
    """SQLite storage for job listings."""

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
                    title TEXT NOT NULL,
                    company TEXT NOT NULL,
                    location TEXT NOT NULL,
                    url TEXT NOT NULL UNIQUE,
                    description TEXT NOT NULL,
                    posted_date TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

    def add_job(self, job: Job | dict[str, str]) -> bool:
        """Insert one job; return False when its URL already exists."""
        values = job.to_dict() if isinstance(job, Job) else job

        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT OR IGNORE INTO jobs
                    (title, company, location, url, description, posted_date)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    values["title"],
                    values["company"],
                    values["location"],
                    values["url"],
                    values["description"],
                    values["posted_date"],
                ),
            )
            return cursor.rowcount == 1

    def add_jobs(self, jobs: Iterable[Job | dict[str, str]]) -> int:
        """Insert jobs using one database connection."""
        inserted = 0

        with self._connect() as connection:
            for job in jobs:
                values = job.to_dict() if isinstance(job, Job) else job

                cursor = connection.execute(
                    """
                    INSERT OR IGNORE INTO jobs
                        (title, company, location, url, description, posted_date)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        values["title"],
                        values["company"],
                        values["location"],
                        values["url"],
                        values["description"],
                        values["posted_date"],
                    ),
                )

                inserted += cursor.rowcount

        return inserted

    def get_jobs(self, limit: int | None = None) -> list[dict[str, str]]:
        """Return stored jobs, newest records first."""
        query = "SELECT * FROM jobs ORDER BY id DESC"
        parameters: tuple[int, ...] = ()

        if limit is not None:
            if limit < 1:
                raise ValueError("limit must be at least 1")
            query += " LIMIT ?"
            parameters = (limit,)

        with self._connect() as connection:
            rows = connection.execute(query, parameters).fetchall()
            return [dict(row) for row in rows]