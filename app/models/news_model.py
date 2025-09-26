from pydantic import BaseModel, HttpUrl
from typing import Optional


class NewsItem(BaseModel):
    """Structured representation of a news result."""
    title: str
    link: HttpUrl
    snippet: Optional[str] = None
    source: Optional[str] = None
