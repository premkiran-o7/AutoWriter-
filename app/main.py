from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="AI LinkedIn Post Generator")

app.include_router(router)



