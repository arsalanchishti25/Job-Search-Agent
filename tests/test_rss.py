from src.job_agent.sources.rss import fetch_jobs_from_rss
from src.job_agent.sources.models import Job

def test_fetch_jobs_from_rss():
    jobs = fetch_jobs_from_rss("https://devitjobs.uk/job_feed.xml")

    assert isinstance(jobs, list)
    assert all(isinstance(j, Job) for j in jobs)

    if jobs:
        job = jobs[0]

        assert job.title
        assert job.url
        assert job.company
        assert job.location is not None
        assert job.description is not None
        assert job.posted_date is not None