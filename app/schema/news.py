from pydantic import BaseModel
from app.models.news_model import NewsItem


class News_List(BaseModel):
    News_List : list[NewsItem]