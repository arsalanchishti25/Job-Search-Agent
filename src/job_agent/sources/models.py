from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class Job:
    title: str
    company: str
    location: str
    url: str
    description: str
    posted_date: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)