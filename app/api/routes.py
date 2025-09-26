from fastapi import APIRouter, HTTPException
from typing import List
from app.agents.news_agent import fetch_news_sources
from app.agents.post_generator import generate_post
from app.models.news_model import NewsItem
from app.models.post_model import LinkedInPost
from app.schema.post_schema import GeneratePostRequest, GeneratePostResponse
from app.utils.logger import logger  # import logger

router = APIRouter()

@router.post("/generate-post", response_model=GeneratePostResponse)
def generate_linkedin_post(request: GeneratePostRequest):
    # log request received
    logger.info(f"Received post generation request for topic: {request.topic}")
    try:
        # fetch news items
        news_items: list[NewsItem] = fetch_news_sources(request.topic, max_results=5)
        if not news_items:
            logger.warning("No news found for topic: %s", request.topic)
            raise HTTPException(status_code=404, detail="No news found for this topic.")

        # generate LinkedIn post
        post: LinkedInPost = generate_post(request.topic, news_items)

        post = post["linkedin_post"] if isinstance(post, dict) and "linkedin_post" in post else post
        # prepare response
        response = GeneratePostResponse(
            topic=post.topic,
            news_sources=[item.link for item in news_items],
            linkedin_post=post.linkedin_post,
            image_suggestion=post.image_suggestion,
        )
        logger.info("Post generated successfully for topic: %s", request.topic)
        return response

    except Exception as e:
        logger.error("Error generating post: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))
