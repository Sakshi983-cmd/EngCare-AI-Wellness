from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import json
import logging
from llm_engine import llm_engine
from stress_analyzer import stress_analyzer

app = FastAPI(
    title="EngCare Backend API",
    description="AI-Powered Engineer Wellness Platform",
    version="1.0.0"
)

logger = logging.getLogger(__name__)

class EmployeeData(BaseModel):
    stress_level: int
    work_hours: int
    breaks_taken: int
    productivity: int
    department: Optional[str] = "Engineering"

class CompanyData(BaseModel):
    department: str
    team_size: int
    avg_stress: float
    attrition_rate: float

@app.get("/")
def read_root():
    return {
        "message": "EngCare Backend API - AI Wellness Platform",
        "version": "1.0.0",
        "status": "active"
    }

@app.post("/analyze-stress")
async def analyze_stress(data: EmployeeData):
    """Analyze employee stress and provide AI recommendations"""
    try:
        # Get ML-based stress analysis
        ml_analysis = stress_analyzer.predict_stress_risk(
            data.work_hours, 
            data.work_hours // 2,  # Estimate meetings
            data.breaks_taken, 
            data.stress_level
        )
        
        # Get LLM wellness advice
        wellness_advice = llm_engine.get_wellness_advice(
            data.stress_level,
            data.work_hours,
            data.breaks_taken,
            data.productivity
        )
        
        return {
            "stress_analysis": ml_analysis,
            "wellness_advice": wellness_advice,
            "immediate_actions": [
                "Take a 5-minute break" if data.stress_level > 6 else "Continue current routine",
                "Drink water and stretch",
                "Practice deep breathing"
            ]
        }
        
    except Exception as e:
        logger.error(f"Error in stress analysis: {e}")
        raise HTTPException(status_code=500, detail="Analysis failed")

@app.post("/company-recommendations")
async def get_company_recommendations(data: CompanyData):
    """Get company-level wellness recommendations"""
    try:
        recommendations = llm_engine.get_company_recommendations(
            data.department,
            data.avg_stress,
            data.attrition_rate
        )
        
        return {
            "department": data.department,
            "recommendations": recommendations,
            "risk_level": "high" if data.avg_stress > 7.0 else "medium" if data.avg_stress > 5.0 else "low"
        }
        
    except Exception as e:
        logger.error(f"Error in company recommendations: {e}")
        raise HTTPException(status_code=500, detail="Recommendation generation failed")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "llm_loaded": llm_engine.chatbot is not None}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
