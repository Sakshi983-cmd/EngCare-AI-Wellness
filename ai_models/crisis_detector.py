import logging
from typing import Dict, List, Any
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class CrisisDetector:
    def __init__(self):
        self.red_flags_thresholds = {
            "extreme_stress": 9,  # Stress level 9-10/10
            "excessive_hours": 12,  # More than 12 hours
            "no_breaks": 0,  # No breaks taken
            "productivity_crash": 3,  # Productivity below 3/10
            "extended_pattern": 5  # Days with concerning patterns
        }
        
        self.crisis_responses = {
            "immediate": [
                "🆘 IMMEDIATE: Contact mental health professional",
                "🆘 Activate emergency support protocol", 
                "🆘 Ensure employee safety and well-being"
            ],
            "high_priority": [
                "🚨 Schedule urgent meeting with HR and manager",
                "🚨 Provide immediate workload reduction",
                "🚨 Connect with company counselor within 24 hours"
            ],
            "medium_priority": [
                "⚠️ Schedule wellness check-in this week",
                "⚠️ Offer flexible work arrangements",
                "⚠️ Provide stress management resources"
            ]
        }
    
    def detect_crisis_patterns(self, employee_data: Dict[str, Any], historical_data: List[Dict] = None) -> Dict[str, Any]:
        """
        Detect potential crisis patterns and provide intervention recommendations
        
        Args:
            employee_data: Current employee data
            historical_data: Historical data for pattern analysis
            
        Returns:
            Dictionary with crisis analysis and recommendations
        """
        try:
            current_stress = employee_data.get('stress_level', 5)
            work_hours = employee_data.get('work_hours', 8)
            breaks_taken = employee_data.get('breaks_taken', 2)
            productivity = employee_data.get('productivity', 7)
            
            risk_factors = self.calculate_risk_factors(
                current_stress, work_hours, breaks_taken, productivity
            )
            
            # Analyze historical patterns if available
            historical_risk = self.analyze_historical_patterns(historical_data)
            total_risk_score = risk_factors['current_risk_score'] + historical_risk
            
            # Determine crisis level
            crisis_level = self.determine_crisis_level(total_risk_score)
            
            # Get appropriate responses
            interventions = self.get_interventions(crisis_level, risk_factors)
            
            return {
                "crisis_level": crisis_level,
                "total_risk_score": total_risk_score,
                "risk_factors": risk_factors['factors'],
                "immediate_actions": interventions['immediate'],
                "follow_up_actions": interventions['follow_up'],
                "monitoring_recommendations": interventions['monitoring'],
                "alert_required": crisis_level in ["immediate", "high_priority"]
            }
            
        except Exception as e:
            logger.error(f"Error in crisis detection: {e}")
            return self.get_fallback_response()
    
    def calculate_risk_factors(self, stress: int, hours: int, breaks: int, productivity: int) -> Dict[str, Any]:
        """Calculate risk factors and score"""
        risk_factors = []
        risk_score = 0
        
        # Extreme stress check
        if stress >= self.red_flags_thresholds["extreme_stress"]:
            risk_factors.append("extreme_stress_detected")
            risk_score += 3
        
        # Excessive work hours
        if hours > self.red_flags_thresholds["excessive_hours"]:
            risk_factors.append("excessive_work_hours")
            risk_score += 2
        
        # No breaks
        if breaks <= self.red_flags_thresholds["no_breaks"]:
            risk_factors.append("insufficient_breaks")
            risk_score += 2
        
        # Productivity crash
        if productivity <= self.red_flags_thresholds["productivity_crash"]:
            risk_factors.append("severe_productivity_drop")
            risk_score += 2
        
        # Multiple risk factors
        if len(risk_factors) >= 3:
            risk_score += 2  # Additional risk for multiple factors
        
        return {
            "current_risk_score": risk_score,
            "factors": risk_factors,
            "risk_count": len(risk_factors)
        }
    
    def analyze_historical_patterns(self, historical_data: List[Dict]) -> int:
        """Analyze historical data for concerning patterns"""
        if not historical_data:
            return 0
        
        try:
            recent_data = historical_data[-7:]  # Last 7 days
            high_stress_days = sum(1 for day in recent_data if day.get('stress_level', 0) >= 8)
            long_hours_days = sum(1 for day in recent_data if day.get('work_hours', 0) > 10)
            
            historical_risk = 0
            if high_stress_days >= 5:
                historical_risk += 2
            if long_hours_days >= 5:
                historical_risk += 2
                
            return historical_risk
            
        except Exception as e:
            logger.error(f"Error in historical analysis: {e}")
            return 0
    
    def determine_crisis_level(self, risk_score: int) -> str:
        """Determine crisis level based on risk score"""
        if risk_score >= 8:
            return "immediate"
        elif risk_score >= 5:
            return "high_priority"
        elif risk_score >= 3:
            return "medium_priority"
        else:
            return "low_priority"
    
    def get_interventions(self, crisis_level: str, risk_factors: Dict) -> Dict[str, List[str]]:
        """Get appropriate interventions based on crisis level"""
        base_actions = self.crisis_responses.get(crisis_level, [])
        
        interventions = {
            "immediate": base_actions,
            "follow_up": [],
            "monitoring": []
        }
        
        # Add specific follow-up actions based on risk factors
        if "extreme_stress_detected" in risk_factors['factors']:
            interventions["follow_up"].append("Schedule weekly counseling sessions")
            interventions["monitoring"].append("Daily stress level check-ins")
        
        if "excessive_work_hours" in risk_factors['factors']:
            interventions["follow_up"].append("Implement strict work hour limits")
            interventions["monitoring"].append("Monitor work hours daily")
        
        if "insufficient_breaks" in risk_factors['factors']:
            interventions["follow_up"].append("Mandatory break reminders")
            interventions["monitoring"].append("Track break frequency")
        
        return interventions
    
    def get_fallback_response(self) -> Dict[str, Any]:
        """Fallback response in case of errors"""
        return {
            "crisis_level": "low_priority",
            "total_risk_score": 2,
            "risk_factors": ["unknown_risk"],
            "immediate_actions": ["Monitor employee well-being"],
            "follow_up_actions": ["Schedule general wellness check-in"],
            "monitoring_recommendations": ["Regular stress level tracking"],
            "alert_required": False
        }

# Global instance
crisis_detector = CrisisDetector()
