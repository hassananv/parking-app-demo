from fastapi import APIRouter

from .routers.user_router import router as user_router
from .routers.auth_router import router as auth_router
from .routers.booking_router import router as booking_router
from .routers.spot_router import router as spot_router


router = APIRouter( prefix="/api/v1",)


router.include_router(user_router)
router.include_router(auth_router)
router.include_router(booking_router)
router.include_router(spot_router)