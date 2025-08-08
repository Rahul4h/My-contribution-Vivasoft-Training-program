from fastapi import FastAPI
from .auth_middleware import AuthMiddleware
from .guest_middleware import GuestMiddleware

def register_middlewares(app: FastAPI):
    app.add_middleware(AuthMiddleware)
    app.add_middleware(GuestMiddleware)
    return app
