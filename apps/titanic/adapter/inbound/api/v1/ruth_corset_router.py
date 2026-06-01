from fastapi import APIRouter


ruth_corset_router = APIRouter(prefix="/ruth-corset", tags=["titanic-ruth-corset"])


@ruth_corset_router.get("/corset")
async def get_corset():
    pass
