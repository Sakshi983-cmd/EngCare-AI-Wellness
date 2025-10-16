import random
import logging
from typing import Dict, List, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class EmployeeCoach:
    def __init__(self):
        self.wellness_tips = {
            "immediate_relief": [
                "🧘 Try 4-7-8 breathing: Inhale 4s, hold 7s, exhale 8s",
                "💧 Drink a glass of cold water and splash face",
                "🚶 Stand up and stretch for 2 minutes",
                "🎵 Listen to one favorite song with eyes closed",
                "✍️ Write down 3 things you're grateful for"
            ],
            "short_break": [
                "🌿 Take 5-minute walk outside or near window",
                "📖 Read something completely unrelated to work", 
                "🎨 Doodle or draw for 5 minutes",
                "🧠 Do a quick puzzle or brain teaser",
                "💝 Send an appreciation message to a colleague"
            ],
            "stress_management": [
                "⏰ Use Pomodoro technique: 25min work, 5min break",
                "📱 Digital detox: No screens for 15 minutes",
                "🥗 Eat a healthy snack with protein and fiber",
                "💬 Talk to a friend or family member for 10 minutes",
                "📝 Journal about your feelings for 5 minutes"
            ],
            "long_term_wellness": [
                "🏃 Establish daily exercise routine (even 15 minutes)",
                "🎯 Set clear work-life boundaries",
                "📅 Schedule 'me time' in your calendar",
                "🌙 Maintain consistent sleep schedule",
                "🍎 Meal prep healthy lunches for the week"
            ]
        }
        
        self.engineer_specific_tips = [
            "🐛 Take a break from debugging and work on something creative",
            "🔧 Practice rubber duck debugging - explain problem aloud",
            "💻 Use blue light filter glasses during long coding sessions",
            "⚡ Implement 'power hour' for focused coding without interruptions",
            "🔄 Try pair programming for complex problems",
            "📚 Learn a new technology through fun side projects",
            "🎮 Take gaming breaks to reset problem-solving mindset"
        ]
    
    def get_personalized_tips(self, employee_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get personalized wellness tips based on employee profile
        
        Args:
            employee_profile: Dictionary containing employee data and preferences
            
        Returns:
            Dictionary with categorized wellness tips
        """
        try:
            stress_level = employee_profile.get('stress_level', 5)
            work_hours = employee_profile.get('work_hours', 8)
            breaks_taken = employee_profile.get('breaks_taken', 2)
            productivity = employee_profile.get('productivity', 7)
            role = employee_profile.get('role', 'engineer')
            current_time = employee_profile.get('current_time', datetime.now().hour)
            
            tips = {
                "immediate_actions": self.get_immediate_tips(stress_level),
                "break_ideas": self.get_break_tips(work_hours, breaks_taken),
                "stress_management": self.get_stress_management_tips(stress_level),
                "long_term_strategies": self.get_long_term_tips(productivity, work_hours),
                "role_specific": self.get_role_specific_tips(role),
                "time_based": self.get_time_based_tips(current_time)
            }
            
            # Add motivational message
            tips["motivational_message"] = self.get_motivational_message(stress_level, productivity)
            
            return tips
            
        except Exception as e:
            logger.error(f"Error generating personalized tips: {e}")
            return self.get_fallback_tips()
    
    def get_immediate_tips(self, stress_level: int) -> List[str]:
        """Get immediate relief tips based on stress level"""
        if stress_level >= 8:
            return random.sample(self.wellness_tips["immediate_relief"], 3)
        elif stress_level >= 6:
            return random.sample(self.wellness_tips["immediate_relief"], 2)
        else:
            return random.sample(self.wellness_tips["immediate_relief"], 1)
    
    def get_break_tips(self, work_hours: int, breaks_taken: int) -> List[str]:
        """Get break ideas based on work hours and breaks taken"""
        tips_needed = max(0, (work_hours // 2) - breaks_taken)  # Suggest more tips if fewer breaks taken
        num_tips = min(3, tips_needed + 1)
        
        return random.sample(self.wellness_tips["short_break"], num_tips)
    
    def get_stress_management_tips(self, stress_level: int) -> List[str]:
        """Get stress management tips based on stress level"""
        if stress_level >= 7:
            return random.sample(self.wellness_tips["stress_management"], 3)
        else:
            return random.sample(self.wellness_tips["stress_management"], 2)
    
    def get_long_term_tips(self, productivity: int, work_hours: int) -> List[str]:
        """Get long-term wellness strategies"""
        tips = random.sample(self.wellness_tips["long_term_wellness"], 2)
        
        if work_hours > 9:
            tips.append("🕒 Set strict 'shutdown' ritual to end work day")
        if productivity < 5:
            tips.append("🎯 Break large tasks into smaller, manageable chunks")
            
        return tips
    
    def get_role_specific_tips(self, role: str) -> List[str]:
        """Get role-specific wellness tips"""
        if role.lower() in ['engineer', 'developer', 'programmer']:
            return random.sample(self.engineer_specific_tips, 2)
        else:
            return ["🎯 Customize your workspace for comfort", "📊 Set realistic daily goals"]
    
    def get_time_based_tips(self, current_hour: int) -> List[str]:
        """Get tips based on time of day"""
        if current_hour < 12:
            return ["🌅 Start day with 5-minute planning session", "🥛 Have protein-rich breakfast"]
        elif current_hour < 17:
            return ["🍎 Have healthy afternoon snack", "👀 Do eye exercises to reduce strain"]
        else:
            return ["🌙 Avoid screens 1 hour before bed", "📖 Read a book instead of scrolling"]
    
    def get_motivational_message(self, stress_level: int, productivity: int) -> str:
        """Get personalized motivational message"""
        if stress_level <= 4 and productivity >= 7:
            messages = [
                "🌟 You're doing amazing! Keep up the great work and maintain this healthy balance!",
                "💪 Perfect equilibrium! Your wellness habits are paying off beautifully!",
                "🎯 Excellent work-life balance! You're setting a great example for others!"
            ]
        elif stress_level >= 7:
            messages = [
                "🤗 It's okay to not be okay. Remember to prioritize your mental health today.",
                "🌧️ Storms don't last forever. Take things one step at a time, you've got this!",
                "❤️ Your well-being matters more than any deadline. Be kind to yourself today."
            ]
        else:
            messages = [
                "🚀 You're making great progress! Small consistent steps lead to big changes!",
                "🌈 Balance is key - remember to celebrate small wins along the way!",
                "💫 Every effort counts! You're building healthier habits every day!"
            ]
        
        return random.choice(messages)
    
    def get_fallback_tips(self) -> Dict[str, Any]:
        """Fallback tips in case of errors"""
        return {
            "immediate_actions": ["Take 5 deep breaths", "Drink some water"],
            "break_ideas": ["Take a short walk", "Stretch for 2 minutes"],
            "stress_management": ["Practice mindfulness", "Take regular breaks"],
            "long_term_strategies": ["Maintain work-life balance", "Get adequate sleep"],
            "role_specific": ["Customize your workspace", "Set clear goals"],
            "time_based": ["Stay hydrated throughout day"],
            "motivational_message": "You're doing great! Remember to take care of yourself."
        }

# Global instance
employee_coach = EmployeeCoach()
