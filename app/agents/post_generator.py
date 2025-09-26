from typing import List
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, END
from pydantic import BaseModel
from app.config import settings
from app.utils.logger import logger  # get logger from utils/logger.py

from app.models.news_model import NewsItem
from app.models.post_model import LinkedInPost
from app.agents.prompts import (
    SUMMARIZER_PROMPT,
    POST_GENERATOR_PROMPT,
    REVIEWER_PROMPT,
)

# State for LangGraph
class WorkflowState(BaseModel):
    topic: str
    news_items: List[NewsItem]
    summary: str = ""
    post: LinkedInPost | None = None

# Setup Gemini LLM
def setup_llm():
    # Initialize LLM
    return init_chat_model("gemini-2.5-flash", model_provider="google_genai", api_key=settings.GOOGLE_API_KEY)

# Summarizer node
def summarizer_node(state: WorkflowState) -> WorkflowState:
    # Summarize news items
    logger.info("Summarizing news items for topic: %s", state.topic)
    llm = setup_llm()
    context = "\n".join([f"- {item.title}: {item.snippet or ''}" for item in state.news_items])
    prompt = SUMMARIZER_PROMPT.format(topic=state.topic, context=context)
    logger.debug("Summarizer prompt: %s", prompt)
    state.summary = llm.invoke(prompt).content
    logger.info("Summary generated.")
    return state

# Post generator node
def post_generator_node(state: WorkflowState) -> WorkflowState:
    # Generate LinkedIn post
    logger.info("Generating LinkedIn post for topic: %s", state.topic)
    llm = setup_llm()
    sources = [item.link for item in state.news_items]
    prompt = POST_GENERATOR_PROMPT.format(topic=state.topic, summary=state.summary)
    logger.debug("Post generator prompt: %s", prompt)
    response = llm.invoke(prompt).content
    post = LinkedInPost(
        topic=state.topic,
        news_sources=sources,
        linkedin_post=response,
        image_suggestion="AI-themed illustration"
    )
    state.post = post
    logger.info("LinkedIn post generated.")
    return state

# Reviewer node
def reviewer_node(state: WorkflowState) -> WorkflowState:
    # Review LinkedIn post
    logger.info("Reviewing LinkedIn post for topic: %s", state.topic)
    llm = setup_llm()
    context = "\n".join([f"- {item.title}: {item.snippet or ''}" for item in state.news_items])
    prompt = REVIEWER_PROMPT.format(
        topic=state.topic,
        sources=context,
        draft_post=state.post.linkedin_post
    )
    logger.debug("Reviewer prompt: %s", prompt)
    reviewed_post = llm.invoke(prompt).content
    logger.info("LinkedIn post reviewed and updated.")
    return state

# Build workflow graph
def build_graph():
    # Construct workflow graph
    logger.info("Building workflow graph.")
    workflow = StateGraph(WorkflowState)
    workflow.add_node("summarizer", summarizer_node)
    workflow.add_node("post_generator", post_generator_node)
    workflow.add_node("reviewer", reviewer_node)
    workflow.set_entry_point("summarizer")
    workflow.add_edge("summarizer", "post_generator")
    workflow.add_edge("post_generator", "reviewer")
    workflow.add_edge("reviewer", END)
    logger.info("Workflow graph built and compiled.")
    return workflow.compile()

# Public API
def generate_post(topic: str, news_items: List[NewsItem]) -> LinkedInPost:
    # Generate reviewed LinkedIn post
    logger.info("Starting post generation for topic: %s", topic)
    graph = build_graph()
    initial_state = WorkflowState(topic=topic, news_items=news_items)
    final_state = graph.invoke(initial_state)
    print(final_state)
    logger.info(type(final_state))
    logger.info("Post generation completed.")
    return final_state["post"]
