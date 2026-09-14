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
    assert jobs[0]["title"] == "Junior Software Engineer"
    assert jobs[0]["company"] == "Example Ltd"


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