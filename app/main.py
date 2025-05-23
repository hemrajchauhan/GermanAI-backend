import os
from fastapi import FastAPI
from app.routers import grammar, translate
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Get allowed origins from environment variable, defaulting to your production domain
allowed_origins = os.getenv("ALLOWED_ORIGINS", "https://germanai-backend.fly.dev")
allowed_origins = [origin.strip() for origin in allowed_origins.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(grammar.router)
app.include_router(translate.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to GermanAI-backend! Visit /docs for API documentation."}

