from pydantic import BaseModel, HttpUrl
from typing import List

class GeneratePostRequest(BaseModel):
    topic: str


class GeneratePostResponse(BaseModel):
    topic: str
    news_sources: List[HttpUrl]
    linkedin_post: str
    image_suggestion: str | None