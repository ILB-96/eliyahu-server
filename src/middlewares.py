# noinspection PyProtectedMember
from slowapi import _rate_limit_exceeded_handler
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from starlette.responses import JSONResponse
from starlette.status import HTTP_403_FORBIDDEN

from .constants import HOST, ORIGIN, URL

class EnforceAllowedOriginsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        origin = request.headers.get("origin") or request.headers.get("referer")
        print(request.headers)
        if origin is None or not any(origin.startswith(o) for o in (ORIGIN, URL)):
            return JSONResponse(
                {"detail": "Origin not allowed"},
                status_code=HTTP_403_FORBIDDEN,
            )

        return await call_next(request)
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        return response

def add_custom_middlewares(app):
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(EnforceAllowedOriginsMiddleware)
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=[HOST])
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.add_middleware(SlowAPIMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=(ORIGIN, URL),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )