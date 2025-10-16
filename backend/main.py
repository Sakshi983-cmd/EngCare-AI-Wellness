from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import json
import os

app = FastAPI(title="EngCare Backend API")

class EmployeeData(BaseModel):
    stress_level: int
    work_hours: int
    breaks_taken: int
    productivity: int

class CompanyData(BaseModel):
    department: str
    team_size: int
    avg_stress: float

@app.get("/")
def read_root():
    return {"message": "EngCare Backend API - AI Wellness Platform"}

@app.post("/analyze-stress")
async def analyze_stress(data: EmployeeData):
    stress_score = (data.stress_level * 10) + (data.work_hours * 2) - (data.breaks_taken * 5)
    stress_score = max(0, min(100, stress_score))
    
    return {
        "stress_score": stress_score,
        "risk_level": "high" if stress_score > 70 else "medium" if stress_score > 40 else "low",
        "recommendations": [
            "Take regular breaks every hour",
            "Practice deep breathing exercises",
            "Stay hydrated throughout the day"
        ]
    }

@app.get("/wellness-resources")
async def get_wellness_resources():
    try:
        with open("data/wellness_resources.json", "r") as f:
            resources = json.load(f)
        return resources
    except:
        return {"error": "Resources not available"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
