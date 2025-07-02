from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import ALLOWED_ORIGINS
from app.routers.grammar.grammar_router import router as grammar_router
from app.routers.translation.translation_router import router as translation_router
from app.routers.dictionary.dictionary_router import router as dictionary_router
from app.routers.protected.keycloak_router import router as keycloak_router
from app.routers.llm.germangpt_router import router as germangpt_router
from app.routers.dictionary.noun_info_router import router as noun_info_router
from app.routers.vocab.dwds_vocab_router import router as dwds_vocab_router

app = FastAPI(
    title="GermanAI-backend",
    description="Open-source backend for German language learning apps. Provides grammar checking, translation, and more.",
    version="1.0.0"
)

allowed_origins = [origin.strip() for origin in ALLOWED_ORIGINS.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Group endpoints by tech/service
app.include_router(grammar_router, prefix="/api/grammar", tags=["Grammar"])
app.include_router(translation_router, prefix="/api/translation", tags=["Translation"])
app.include_router(dictionary_router, prefix="/api/dictionary", tags=["Dictionary"])
app.include_router(noun_info_router, prefix="/api/dictionary", tags=["Dictionary"])
app.include_router(dwds_vocab_router, prefix="/api/dwds", tags=["DWDS Vocabulary"])
app.include_router(germangpt_router, prefix="/api/llm/germangpt", tags=["GermanGPT"])
app.include_router(keycloak_router, prefix="/api/protected", tags=["Keycloak"])

@app.get("/")
def read_root():
    return {"message": "Welcome to GermanAI-backend! Visit /docs for API documentation."}

@app.get("/health")
def health():
    return {"status": "ok"}
