from fastapi import APIRouter


jack_sketch_router = APIRouter(prefix="/jack-sketch", tags=["titanic-jack-sketch"])


@jack_sketch_router.get("/sketch")
async def get_sketch():
    pass
