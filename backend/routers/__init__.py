from backend.routers.auth import router as auth_router
from backend.routers.clients import router as client_router
from backend.routers.admin import router as admin_router
from backend.routers.tasks import router as task_router
from backend.routers.documents import router as doc_router
from backend.routers.reports import router as reports_router

__all__ = ["auth_router", "client_router", "admin_router", "task_router", "doc_router", "reports_router"]
