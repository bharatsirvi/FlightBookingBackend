from fastapi import FastAPI
from app.api.routes import router
from fastapi.middleware.cors import CORSMiddleware
import logging
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO)

app = FastAPI()
origins = [
    "http://localhost:5173",  # Vite dev server
    "http://127.0.0.1:5173",  # alternative form
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,             # or ["*"] for all origins (not recommended for production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")
