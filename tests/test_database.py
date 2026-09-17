from src.job_agent.sources.models import Job
from src.job_agent.storage.database import JobDatabase


def make_job(url: str = "https://example.com/jobs/1") -> Job:
    return Job(
        title="Junior Software Engineer",
        company="Example Ltd",
        location="Manchester",
        url=url,
        description="Python and cloud development",
        posted_date="2026-09-15",
    )


def test_database_creates_and_stores_job(tmp_path):
    database = JobDatabase(tmp_path / "jobs.db")

    assert database.add_job(make_job()) is True

    jobs = database.get_jobs()
    assert len(jobs) == 1

    row = jobs[0]
    assert row["job_title"] == "Junior Software Engineer"
    assert row["company_name"] == "Example Ltd"
    assert row["location"] == "Manchester"
    assert row["description"] == "Python and cloud development"
    assert row["match_score"] is None
    assert row["match_explanation"] is None
    assert row["verification_status"] == "unverified"
    assert row["generated_cv_filename"] is None
    assert "created_at" in row
    assert "updated_at" in row


def test_duplicate_url_is_ignored(tmp_path):
    database = JobDatabase(tmp_path / "jobs.db")
    job = make_job()

    assert database.add_job(job) is True
    assert database.add_job(job) is False
    assert len(database.get_jobs()) == 1


def test_add_jobs_returns_number_of_new_jobs(tmp_path):
    database = JobDatabase(tmp_path / "jobs.db")

    inserted = database.add_jobs(
        [
            make_job("https://example.com/jobs/1"),
            make_job("https://example.com/jobs/2"),
            make_job("https://example.com/jobs/1"),
        ]
    )

    assert inserted == 2
    assert len(database.get_jobs()) == 2


def test_update_job_match(tmp_path):
    database = JobDatabase(tmp_path / "jobs.db")
    job = make_job()

    database.add_job(job)

    database.update_job_match(
        job_url=job.url,
        match_score=0.85,
        match_explanation="Strong match on Python and cloud skills",
    )

    rows = database.get_jobs()
    assert len(rows) == 1
    row = rows[0]

    assert row["match_score"] == 0.85
    assert row["match_explanation"] == "Strong match on Python and cloud skills"
    assert row["updated_at"] != row["created_at"]


def test_update_job_verification(tmp_path):
    database = JobDatabase(tmp_path / "jobs.db")
    job = make_job()

    database.add_job(job)
    database.update_job_verification(job_url=job.url, verification_status="verified")

    rows = database.get_jobs()
    assert len(rows) == 1
    assert rows[0]["verification_status"] == "verified"


def test_update_job_cv_filename(tmp_path):
    database = JobDatabase(tmp_path / "jobs.db")
    job = make_job()

    database.add_job(job)

    cv_filename = "Example_Ltd_Junior_Software_Engineer_1.txt"
    database.update_job_cv_filename(job_url=job.url, generated_cv_filename=cv_filename)

    rows = database.get_jobs()
    assert len(rows) == 1
    assert rows[0]["generated_cv_filename"] == cv_filename


def test_get_jobs_limit(tmp_path):
    database = JobDatabase(tmp_path / "jobs.db")

    database.add_jobs(
        [
            make_job(f"https://example.com/jobs/{i}")
            for i in range(1, 6)
        ]
    )

    all_jobs = database.get_jobs()
    assert len(all_jobs) == 5

    limited = database.get_jobs(limit=3)
    assert len(limited) == 3
    # Should be newest first (highest id first)
    assert limited[0]["id"] == 5
    assert limited[1]["id"] == 4
    assert limited[2]["id"] == 3


def test_get_jobs_limit_invalid(tmp_path):
    database = JobDatabase(tmp_path / "jobs.db")

    import pytest
    import sqlite3

    # Ensure ValueError for limit < 1
    try:
        database.get_jobs(limit=0)
        assert False, "Expected ValueError for limit < 1"
    except ValueError:
        pass

    try:
        database.get_jobs(limit=-5)
        assert False, "Expected ValueError for negative limit"
    except ValueError:
        pass