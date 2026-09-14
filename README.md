# Job Search Agent

A personal agent for finding, verifying and ranking relevant job opportunities against a CV and portfolio.

## Initial structure

- `src/job_agent/sources/` — job feeds, APIs and permitted scrapers.
- `src/job_agent/storage/` — SQLite database operations.
- `src/job_agent/matching/` — CV and job relevance scoring.
- `src/job_agent/verification/` — checks whether job links and postings remain active.
- `src/job_agent/cv_tailoring/` — creates tailored CV versions.
- `src/job_agent/reporting/` — produces CSV, HTML or PDF reports.
- `src/job_agent/scheduling/` — daily execution logic.
- `data/` — local input and database files.
- `reports/` — generated reports and tailored CVs.
- `tests/` — automated tests.

## Setup

```powershell
python -m venv .venv
.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
pytest
python -m src.job_agent.main
```

Do not commit personal CVs, credentials or generated reports.
