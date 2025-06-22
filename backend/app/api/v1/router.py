from fastapi import APIRouter
from .endpoints import auth, dashboard, documents, search, notifications, analytics, users

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(documents.router, prefix="/documents", tags=["Documents"])
api_router.include_router(search.router, prefix="/search", tags=["Search"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])

# TODO: Add other endpoint routers when they are created:
# api_router.include_router(reviews.router, prefix="/reviews", tags=["Reviews"])
# api_router.include_router(departments.router, prefix="/departments", tags=["Departments"])
# api_router.include_router(audit.router, prefix="/audit", tags=["Audit Logs"])
