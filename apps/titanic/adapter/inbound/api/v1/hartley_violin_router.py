from fastapi import APIRouter


hartley_violin_router = APIRouter(prefix="/hartley-violin", tags=["titanic-hartley-violin"])


@hartley_violin_router.get("/violin")
async def get_violin():
    pass