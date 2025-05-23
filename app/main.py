from fastapi import FastAPI
from app.routers import grammar, translate

app = FastAPI()
app.include_router(grammar.router)
app.include_router(translate.router)
