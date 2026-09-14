"""Application entry point for the Job Search Agent."""
from src.job_agent.sources.rss import fetch_jobs_from_rss
from src.job_agent.storage.database import JobDatabase


FEED_URL = "https://devitjobs.uk/job_feed.xml"


def main() -> None:
    print("Fetching jobs...")
    jobs = fetch_jobs_from_rss(FEED_URL)

    database = JobDatabase("data/jobs.db")
    new_jobs = database.add_jobs(jobs)

    print(f"Jobs fetched: {len(jobs)}", flush=True)
    print(f"New jobs stored: {new_jobs}")
    print(f"Total jobs in database: {len(database.get_jobs())}")


if __name__ == "__main__":
    main()