from src.handlers.start import router as start_router
from src.handlers.fallback import router as fallback_router

all_routers = [
    start_router,
    fallback_router,
]
