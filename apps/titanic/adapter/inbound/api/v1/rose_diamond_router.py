from fastapi import APIRouter


rose_diamond_router = APIRouter(prefix="/rose-diamond", tags=["titanic-rose-diamond"])


@rose_diamond_router.get("/diamond")
async def get_diamond():
    pass
