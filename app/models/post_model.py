from typing import List, Optional
from pydantic import BaseModel, HttpUrl


class LinkedInPost(BaseModel):
    """Structured LinkedIn-style post output."""
    topic: str
    news_sources: List[HttpUrl]
    linkedin_post: str
    image_suggestion: Optional[str] = None
