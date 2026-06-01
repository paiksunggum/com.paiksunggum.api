from fastapi import APIRouter


isidor_bed_router = APIRouter(prefix="/isidor-bed", tags=["titanic-isidor-bed"])


@isidor_bed_router.get("/bed")
async def get_bed():
    pass
