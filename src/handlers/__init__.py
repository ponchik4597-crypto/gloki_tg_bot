from src.handlers.catalog import router as catalog_router
from src.handlers.company import router as company_router
from src.handlers.fallback import router as fallback_router
from src.handlers.order import router as order_router
from src.handlers.request import router as request_router
from src.handlers.start import router as start_router

all_routers = [
    start_router,
    catalog_router,
    order_router,
    request_router,
    company_router,
    fallback_router,
]
