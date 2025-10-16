from fastapi import APIRouter

router = APIRouter()

@router.get("/test")
def test_profiles():
    return {"message": "Profiles service OK ✅"}
