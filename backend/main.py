from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Retail Analytics System Running"}

@app.get("/detect")
def detect():
    return {
        "people_count": 5,
        "status": "Detection Working"
    }

@app.get("/analytics")
def analytics():
    return {
        "total_visitors": 120,
        "peak_hour": "6 PM"
    }