import logging
from fastapi import FastAPI
from dotenv import load_dotenv
from .payments import router
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://adrateliyahu.com", "https://hsf0dg-uz.myshopify.com"],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app.include_router(router=router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
