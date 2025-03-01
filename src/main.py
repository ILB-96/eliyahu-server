import logging
from fastapi import FastAPI
from dotenv import load_dotenv
from .payments import router

load_dotenv()
app = FastAPI()

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app.include_router(router=router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
