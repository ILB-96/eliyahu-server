from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from dotenv import load_dotenv
import httpx

from src.payments.constants import ACCESS_TOKEN
from .payments import router
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from starlette.middleware.trustedhost import TrustedHostMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
hosts = ("https://adrateliyahu.com", "https://hsf0dg-uz.myshopify.com")


logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

load_dotenv()
limiter = Limiter(key_func=get_remote_address, default_limits=["10/minute"])
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
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(CORSMiddleware,
    allow_origins=hosts,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["eliyahu-server-e0a45d608135.herokuapp.com"])


app.include_router(router=router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
