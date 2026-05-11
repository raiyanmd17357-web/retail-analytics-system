from fastapi import FastAPI
from backend.routes.routes import router

app = FastAPI()

app.include_router(router)