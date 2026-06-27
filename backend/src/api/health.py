from fastapi import APIRouter

router = APIRouter()

@router.get("/", tags=["health"])
async def health_check():
    return {"status": "ok", "message": "Enterprise Knowledge Assistant is running."}
