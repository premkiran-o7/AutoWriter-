from typing import List
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_community.tools import DuckDuckGoSearchResults
from app.schema.news import News_List
from app.models.news_model import NewsItem
from app.utils.logger import logger


def setup_search_agent(max_results: int = 5, time_window: str = "d"):
    """
    Configure DuckDuckGo search agent for Indian news.
    """
    # Initialize DuckDuckGo API wrapper with region and time window
    wrapper = DuckDuckGoSearchAPIWrapper(
        region="in-en",
        time=time_window,
        max_results=max_results
    )
    # Return search results tool
    return DuckDuckGoSearchResults(api_wrapper=wrapper, source="news",output_format="list")


def fetch_news_sources(topic: str, max_results: int = 5) -> List[NewsItem]:
    """
    Fetch recent Indian news sources for a given topic.
    Falls back from last day → last week → last month if no results.

    Args:
        topic (str): The search query/topic.
        max_results (int): Maximum number of results to fetch.

    Returns:
        List[NewsItem]: Structured list of news articles.
    """
    time_windows = ["d", "w", "m"]  # day, week, month

    logger.info(f"Fetching news for topic: '{topic}' with max_results={max_results}")

    for window in time_windows:
        logger.debug(f"Trying time window: '{window}'")
        search = setup_search_agent(max_results=max_results, time_window=window)
        results = search.invoke(topic)  # Invoke search

        logger.info(f"Search results type: {type(results)}")
        logger.info(f"Search results content: {results}")

        news_items: List[NewsItem] = []
        # Parse results if it's a list
        if isinstance(results, list):
            for r in results:
                if isinstance(r, dict) and "link" in r:
                    news_items.append(
                        NewsItem(
                            title=r.get("title", "Untitled"),
                            link=r["link"],
                            snippet=r.get("snippet"),
                            source=r.get("source")
                        )
                    )
        # Parse results if it's a dict
        elif isinstance(results, dict) and "link" in results:
            news_items.append(
                NewsItem(
                    title=results.get("title", "Untitled"),
                    link=results["link"],
                    snippet=results.get("snippet"),
                    source=results.get("source")
                )
            )

        # Return as soon as we get results
        if news_items:
            logger.info(f"Found {len(news_items)} news items for window '{window}'")
            return news_items

        logger.debug(f"No results found for window '{window}'")

    # No results found after all time windows
    logger.warning(f"No news found for topic: '{topic}'")
    return []
