import logging
from fastapi import FastAPI, Request
from dotenv import load_dotenv
from .payments import router
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from starlette.middleware.trustedhost import TrustedHostMiddleware

hosts = ("https://adrateliyahu.com", "https://hsf0dg-uz.myshopify.com")


logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

load_dotenv()
app = FastAPI()

app.add_middleware(CORSMiddleware,
    allow_origins=hosts,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["eliyahu-server-e0a45d608135.herokuapp.com"])

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        {"error": "Too many requests, slow down!"}, status_code=429
    )
app.include_router(router=router)
@app.get("/")
async def root():
    return {"message": "Hello World"}
