from fastapi import APIRouter


smith_captain_router = APIRouter(prefix="/smith-captain", tags=["titanic-smith-captain"])


@smith_captain_router.get("/captain")
async def get_captain():
    pass
