from src.job_agent.sources.rss import fetch_jobs_from_rss


def test_fetch_jobs_from_rss():
    jobs = fetch_jobs_from_rss(
        "https://devitjobs.uk/job_feed.xml"
    )

    assert isinstance(jobs, list)

    if jobs:
        job = jobs[0]

        assert job["title"]
        assert job["url"]
        assert "company" in job
        assert "location" in job
        assert "description" in job
        assert "posted_date" in job