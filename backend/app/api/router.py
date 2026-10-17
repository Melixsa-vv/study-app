from fastapi import APIRouter
from app.api.routes import users, auth, participant, session, admin

api_router = APIRouter()

api_router.include_router(
    auth.router, 
    prefix="/auth", 
    tags=["auth"]
)

api_router.include_router(
    admin.router, 
    prefix="/admin", 
    tags=["admin"]
)

api_router.include_router(
    users.router, 
    prefix="/users", 
    tags=["users"]
)

api_router.include_router(
    session.router,
    prefix="/session", 
    tags=["session"]
)

api_router.include_router(
    participant.router, 
    prefix="/participant", 
    tags=["participant"]
) 