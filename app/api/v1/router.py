from fastapi import APIRouter

from app.api.v1 import auth, users

api_router = APIRouter()


@api_router.get("/ping", tags=["health"])
def ping():
    return {"message": "pong"}


# Auth routes
api_router.include_router(auth.router, prefix="/auth")

# User routes (protected)
api_router.include_router(users.router)
