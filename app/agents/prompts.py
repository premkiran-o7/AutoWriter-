# Summarizer prompt template
SUMMARIZER_PROMPT = (
    "Summarize the following news items on '{topic}' into a concise, "
    "neutral digest for context building:\n\n{context}"
)

# Post generator prompt template
POST_GENERATOR_PROMPT = (
    "Topic: {topic}\n\n"
    "Summary:\n{summary}\n\n"
    "Write a LinkedIn-style post in a professional and engaging tone. "
    "Do not hallucinate facts, only use the summary as source.\n\n"
)

# Reviewer prompt template
REVIEWER_PROMPT = (
    "Review the following LinkedIn post for accuracy.\n\n"
    "Topic: {topic}\n\n"
    "Sources:\n{sources}\n\n"
    "Post Draft:\n{draft_post}\n\n"
    "If the post contains hallucinations or incorrect claims, rewrite it "
    "faithfully based only on the sources. Otherwise, keep it as is."
)
