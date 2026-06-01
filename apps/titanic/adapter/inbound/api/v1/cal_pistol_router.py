from fastapi import APIRouter


cal_pistol_router = APIRouter(prefix="/cal-pistol", tags=["titanic-cal-pistol"])


@cal_pistol_router.get("/pistol")
async def get_pistol():
    pass
