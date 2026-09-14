from src.job_agent.storage.database import JobDatabase

database = JobDatabase("data/jobs.db")

for number, job in enumerate(database.get_jobs(limit=10), start=1):
    print(f"\n{number}. {job['title']}")
    print(f"Company: {job['company']}")
    print(f"Location: {job['location']}")
    print(f"URL: {job['url']}")
    print(f"Posted: {job['posted_date']}")