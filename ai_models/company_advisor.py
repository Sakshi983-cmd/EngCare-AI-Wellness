import json
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class CompanyAdvisor:
    def __init__(self):
        self.wellness_policies = [
            {
                "name": "Flexible Work Hours",
                "description": "Allow employees to choose work timing between 7 AM to 7 PM",
                "impact": "Reduces commute stress, improves work-life balance",
                "implementation_cost": "low"
            },
            {
                "name": "Mental Health Days", 
                "description": "Provide 2 additional paid leaves specifically for mental health",
                "impact": "Prevents burnout, shows organizational care",
                "implementation_cost": "low"
            },
            {
                "name": "Wellness Workshops",
                "description": "Monthly mental health and stress management sessions",
                "impact": "Builds mental health awareness and coping skills", 
                "implementation_cost": "medium"
            },
            {
                "name": "Quiet Rooms",
                "description": "Designated quiet spaces for relaxation and meditation",
                "impact": "Provides immediate stress relief during work hours",
                "implementation_cost": "medium"
            },
            {
                "name": "Team Building Activities",
                "description": "Regular team outings and bonding activities",
                "impact": "Improves team cohesion and reduces workplace tension",
                "implementation_cost": "medium"
            }
        ]
        
        self.department_specific_advice = {
            "Engineering": [
                "Implement 'No Meeting Wednesdays' for deep work",
                "Provide ergonomic chair and desk assessments",
                "Offer technical training to reduce skill stress"
            ],
            "Design": [
                "Creative freedom with clear deadlines",
                "Regular design critique sessions", 
                "Access to latest design tools and resources"
            ],
            "Marketing": [
                "Realistic campaign timelines",
                "Clear KPIs and success metrics",
                "Regular market trend updates"
            ],
            "Sales": [
                "Reasonable sales targets",
                "Team-based incentives",
                "Stress management for client interactions"
            ]
        }
    
    def get_company_recommendations(self, department_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get AI-powered recommendations for company wellness policies
        
        Args:
            department_data: Dictionary containing department metrics
            
        Returns:
            Dictionary with recommendations and insights
        """
        try:
            department = department_data.get('department', 'Engineering')
            avg_stress = department_data.get('avg_stress', 5.0)
            attrition_rate = department_data.get('attrition_rate', 10.0)
            team_size = department_data.get('team_size', 50)
            
            recommendations = []
            urgency_level = "low"
            
            # Analyze stress levels and provide recommendations
            if avg_stress >= 8.0:
                urgency_level = "critical"
                recommendations.extend([
                    "🚨 IMMEDIATE: Implement mandatory stress management program",
                    "🚨 Conduct one-on-one wellness check-ins with all team members", 
                    "🚨 Review and adjust workload distribution immediately"
                ])
            elif avg_stress >= 6.5:
                urgency_level = "high"
                recommendations.extend([
                    "⚠️ Schedule weekly team wellness sessions",
                    "⚠️ Introduce flexible work-from-home options",
                    "⚠️ Provide access to professional counseling services"
                ])
            
            # Analyze attrition and provide recommendations
            if attrition_rate >= 20.0:
                urgency_level = "critical" if urgency_level != "critical" else "critical"
                recommendations.extend([
                    "🔍 Conduct detailed exit interviews to identify root causes",
                    "💡 Implement retention bonus and career growth plans",
                    "🤝 Improve manager training for better team support"
                ])
            elif attrition_rate >= 15.0:
                urgency_level = "high" if urgency_level == "low" else urgency_level
                recommendations.extend([
                    "📊 Analyze workload distribution across team",
                    "🎯 Create clear career progression paths", 
                    "❤️ Enhance employee recognition programs"
                ])
            
            # Add department-specific recommendations
            dept_advice = self.department_specific_advice.get(department, [])
            recommendations.extend(dept_advice[:2])  # Add top 2 department-specific tips
            
            # Add general wellness policies based on team size
            if team_size > 100:
                recommendations.extend([
                    "🏢 Establish dedicated wellness committee",
                    "📱 Implement company-wide wellness mobile app",
                    "🎓 Provide mental health first aid training for managers"
                ])
            else:
                recommendations.extend([
                    "👥 Start weekly team lunch gatherings",
                    "🌱 Create peer support buddy system",
                    "📝 Implement simple anonymous feedback system"
                ])
            
            # Calculate wellness score
            wellness_score = self.calculate_wellness_score(avg_stress, attrition_rate)
            
            return {
                "department": department,
                "urgency_level": urgency_level,
                "wellness_score": wellness_score,
                "recommendations": recommendations[:6],  # Return top 6 recommendations
                "key_metrics": {
                    "current_stress": avg_stress,
                    "attrition_rate": attrition_rate,
                    "team_size": team_size
                },
                "suggested_policies": self.get_relevant_policies(urgency_level, team_size)
            }
            
        except Exception as e:
            logger.error(f"Error in company recommendations: {e}")
            return self.get_fallback_recommendations()
    
    def calculate_wellness_score(self, avg_stress: float, attrition_rate: float) -> int:
        """Calculate overall wellness score (0-100)"""
        stress_score = max(0, 100 - (avg_stress * 10))  # Convert stress to score
        attrition_score = max(0, 100 - (attrition_rate * 4))  # Convert attrition to score
        
        wellness_score = (stress_score * 0.6) + (attrition_score * 0.4)  # Weighted average
        return int(max(0, min(100, wellness_score)))
    
    def get_relevant_policies(self, urgency_level: str, team_size: int) -> List[Dict]:
        """Get relevant wellness policies based on urgency and team size"""
        if urgency_level == "critical":
            return [policy for policy in self.wellness_policies if policy['implementation_cost'] in ['low', 'medium']][:3]
        elif urgency_level == "high":
            return [policy for policy in self.wellness_policies if policy['implementation_cost'] == 'low'][:2]
        else:
            return [policy for policy in self.wellness_policies][:2]  # All policies for low urgency
    
    def get_fallback_recommendations(self) -> Dict[str, Any]:
        """Fallback recommendations in case of errors"""
        return {
            "department": "General",
            "urgency_level": "medium",
            "wellness_score": 65,
            "recommendations": [
                "Implement flexible work hours",
                "Provide mental health resources",
                "Conduct regular team feedback sessions"
            ],
            "key_metrics": {
                "current_stress": 5.0,
                "attrition_rate": 10.0,
                "team_size": 50
            },
            "suggested_policies": self.wellness_policies[:2]
        }

# Global instance
company_advisor = CompanyAdvisor()
