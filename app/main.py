import os
from fastapi import FastAPI
from app.routers import grammar, translate
from app.routers import protected as keycloak_router
# from app.services.keycloak_service import keycloak
from fastapi.middleware.cors import CORSMiddleware

print("Loaded secret")

app = FastAPI(
    title="GermanAI-backend",
    description="Open-source backend for German language learning apps. Provides grammar checking, translation, and more.",
    version="1.0.0"
)

print("Loaded secret:", os.environ.get("KEYCLOAK_CLIENT_SECRET"))

# Read allowed origins from environment variable; defaults to none
allowed_origins = os.getenv("ALLOWED_ORIGINS", "")
allowed_origins = [origin.strip() for origin in allowed_origins.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,    # Set via environment variable!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(grammar.router, tags=["Grammar"])
app.include_router(translate.router, tags=["Translation"])
app.include_router(keycloak_router.router, tags=["Keycloak"])
# # Mount Keycloak's built-in auth endpoints
# app.include_router(keycloak.get_auth_router(), prefix="/auth")


@app.get("/")
def read_root():
    return {"message": "Welcome to GermanAI-backend! Visit /docs for API documentation."}

@app.get("/health")
def health():
    return {"status": "ok"}
