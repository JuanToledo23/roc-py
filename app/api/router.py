from fastapi import APIRouter

from app.api.routers import (
    application,
    auth,
    buildings,
    favorites,
    payment_methods,
    personal_information,
    preferences,
    rooms,
    stripe,
    subscriptions,
    users,
    zones,
    veriff,
)

router = APIRouter(
    prefix="/v1",
)

router.include_router(application.router)
router.include_router(buildings.router)
router.include_router(favorites.router)
router.include_router(auth.router)
router.include_router(payment_methods.router)
router.include_router(stripe.router)
router.include_router(personal_information.router)
router.include_router(preferences.router)
router.include_router(users.router)
router.include_router(rooms.router)
router.include_router(subscriptions.router)
router.include_router(zones.router)
router.include_router(veriff.router)
