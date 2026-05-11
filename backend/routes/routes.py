from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def home():
    return {"message": "Retail Analytics System Running"}

@router.get("/detect")
def detect():
    return {
        "people_count": 5,
        "status": "Detection Working"
    }

@router.get("/analytics")
def analytics():
    return {
        "total_visitors": 120,
        "peak_hour": "6 PM"
    }