from fastapi import APIRouter

router = APIRouter()

@router.post("/")
async def update_item():
    return {"message": "Admin getting schwifty"}