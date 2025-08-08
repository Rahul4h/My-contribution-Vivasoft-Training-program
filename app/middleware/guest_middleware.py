from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, RedirectResponse

# Allow access to guest-only routes for non-authenticated users
class GuestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if (
            hasattr(request.state, "is_authenticated")
            and request.state.is_authenticated
        ):
            return JSONResponse(
                status_code=403, content={"detail": "Already authenticated"}
            )

        return await call_next(request)
