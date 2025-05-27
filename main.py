from fastapi import FastAPI
from app.api.routes import router
import logging
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO)

app = FastAPI()
app.include_router(router, prefix="/api")
