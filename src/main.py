from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import load_dotenv
import httpx

from .constants import ACCESS_TOKEN
from .payments import router
from slowapi import Limiter
from slowapi.util import get_remote_address
from .middlewares import add_custom_middlewares

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
    
    limiter = Limiter(key_func=get_remote_address, default_limits=["10/minute"])
    app.state.limiter = limiter
    
    app.include_router(router=router)
    yield
    await client.aclose()

app = FastAPI(lifespan=lifespan)
add_custom_middlewares(app)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Yeshivat Adrat Eliyahu API"}
