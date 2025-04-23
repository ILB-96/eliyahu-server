from contextlib import asynccontextmanager
from typing import cast

from fastapi import FastAPI
from dotenv import load_dotenv
import httpx
from httpx import AsyncClient

from .constants import ACCESS_TOKEN
from .payments import router
from slowapi import Limiter
from slowapi.util import get_remote_address
from .middlewares import add_custom_middlewares
from starlette.datastructures import State

load_dotenv()
class AppState:
    client: AsyncClient
    limiter: Limiter

@asynccontextmanager
async def lifespan(app_router: FastAPI):
    client = httpx.AsyncClient(
            verify=True,
            headers={
                "Content-Type": "application/json",
                "X-Shopify-Access-Token": ACCESS_TOKEN,
            },
        )
    limiter = Limiter(key_func=get_remote_address, default_limits=["10/minute"])

    app_router.state = cast(State, AppState())
    app_router.state.client = client
    app_router.state.limiter = limiter
    app_router.include_router(router=router)
    
    yield
    await client.aclose()

app = FastAPI(lifespan=lifespan)
add_custom_middlewares(app)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Yeshivat Adrat Eliyahu API"}
