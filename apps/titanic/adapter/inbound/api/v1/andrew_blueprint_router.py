from fastapi import APIRouter


andrew_blueprint_router = APIRouter(prefix="/andrew-blueprint", tags=["titanic-andrew-blueprint"])

@andrew_blueprint_router.get("/blueprint")
async def get_blueprint():
    pass
