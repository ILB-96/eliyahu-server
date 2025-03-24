from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from dotenv import load_dotenv
import httpx

from .constants import ACCESS_TOKEN
from .payments import router
from slowapi import Limiter
from slowapi.util import get_remote_address
from .middlewares import add_custom_middlewares


logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    client = httpx.AsyncClient(
        verify=True,
        headers={
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": ACCESS_TOKEN,
        },
    )
    app.state.client = client
    yield
    await client.aclose()

app = FastAPI(lifespan=lifespan)

limiter = Limiter(key_func=get_remote_address, default_limits=["10/minute"])
app.state.limiter = limiter

add_custom_middlewares(app)

app.include_router(router=router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
