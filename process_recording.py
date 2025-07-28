from fastapi import APIRouter

process_router = APIRouter()

@process_router.post("/process-audio/")
async def process_audio():
    return {"status": "ok"}
