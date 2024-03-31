from fastapi import APIRouter

router=APIRouter()

@router.get("/users")
async def get_users():
    return "no users yet"