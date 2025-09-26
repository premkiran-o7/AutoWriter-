# AI-Powered LinkedIn Post Generator

Generate LinkedIn-style posts from recent news using Google Gemini and LangChain, served via FastAPI.

---

## Prerequisites

- Python 3.11+
- [`uv`](https://github.com/astral-sh/uv) (Python package manager)
- Google Gemini API key

---

## Getting Started

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd <your-repo-directory>
```

### 2. Configure Environment

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
LLM_MODEL=gemini-pro
MAX_NEWS_RESULTS=5
```

### 3. Install Dependencies

```bash
uv install
```

Installs packages from `pyproject.toml` (or `requirements.txt`).

### 4. Run the API Server

```bash
uv run app.main:app --reload
```

- Hot-reload enabled for development.
- API available at [http://127.0.0.1:8000](http://127.0.0.1:8000)

### 5. Test the API

- Open Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Example request to `/generate-post`:

```json
{
    "topic": "Artificial Intelligence"
}
```

- Example response:

```json
{
    "topic": "Artificial Intelligence",
    "news_sources": [
        "https://www.livemint.com/ai-news",
        "https://www.hindustantimes.com/ai-policy"
    ],
    "linkedin_post": "Artificial Intelligence is transforming industries in India...",
    "image_suggestion": "AI-themed illustration"
}
```

### 6. Run Tests

```bash
uv run -m pytest app/tests/test_api.py
```

Tests endpoint functionality and edge cases.

### 7. Logging

- Console logging by default.
- Use the logger in `app/utils/logger.py`:

```python
from app.utils.logger import logger
logger.info("Fetching news...")
logger.error("Failed to generate post")
```

---

