from __future__ import annotations

import html
import re
import urllib.request
import xml.etree.ElementTree as ET

from .models import Job

def clean_text(value: str) -> str:
    value = html.unescape(value)
    value = re.sub(r"<[^>]+>", " ", value)
    return " ".join(value.split())

def fetch_jobs_from_rss(feed_url: str) -> list[Job]:
    request = urllib.request.Request(
        feed_url,
        headers={"User-Agent": "JobSearchAgent/0.1"},
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        xml_content = response.read()

    root = ET.fromstring(xml_content)
    jobs: list[Job] = []

    for item in root.iter():
        fields = {
            child.tag.split("}")[-1].lower(): clean_text(child.text or "")
            for child in item
        }

        title = fields.get("title", "")
        url = fields.get("link", "") or fields.get("url", "")
        company = fields.get("company", "Unknown")
        location = fields.get("location", "Not specified")
        description = fields.get("description", "") or fields.get("summary", "")
        posted_date = fields.get("pubdate", "") or fields.get("published", "Unknown")

        if title and url:
            jobs.append(
                Job(
                    title=title,
                    company=company,
                    location=location,
                    url=url,
                    description=description,
                    posted_date=posted_date,
                )
            )

    return jobs