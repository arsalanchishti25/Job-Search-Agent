# tests/test_ingestion.py

from src.job_agent.sources.rss import fetch_jobs_from_rss
from src.job_agent.storage.database import JobDatabase

# Use the same DB path as your main app, or a dedicated test DB if you prefer.
TEST_DB_PATH = "data/jobs.db"


def test_ingest_rss_into_database():
    db = JobDatabase(TEST_DB_PATH)

    # Fetch jobs from the feed
    jobs = fetch_jobs_from_rss("https://devitjobs.uk/job_feed.xml")
    assert isinstance(jobs, list)

    # Collect URLs so we can clean them up later
    inserted_urls = [job.url for job in jobs]

    try:
        first_insert = db.add_jobs(jobs)
        assert first_insert >= 0

        total_after_insert = len(db.get_jobs())
        assert total_after_insert >= first_insert

        # Insert again – duplicates should be ignored
        second_insert = db.add_jobs(jobs)
        assert second_insert == 0
        assert len(db.get_jobs()) == total_after_insert
    finally:
        # Clean up: remove the jobs we inserted in this test
        with db._connect() as connection:
            # Build placeholders safely
            placeholders = ",".join("?" for _ in inserted_urls)
            connection.execute(
                f"DELETE FROM jobs WHERE job_url IN ({placeholders})",
                inserted_urls,
            )