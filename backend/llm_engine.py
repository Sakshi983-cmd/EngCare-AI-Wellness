from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMEngine:
    def __init__(self):
        self.chatbot = None
        self.setup_model()
    
    def setup_model(self):
        """Initialize the LLM model"""
        try:
            logger.info("Loading DialoGPT model for wellness coaching...")
            self.chatbot = pipeline(
                "text-generation",
                model="microsoft/DialoGPT-medium",
                tokenizer="microsoft/DialoGPT-medium",
                max_length=200,
                do_sample=True,
                temperature=0.7,
                pad_token_id=50256
            )
            logger.info("LLM model loaded successfully!")
        except Exception as e:
            logger.error(f"Failed to load LLM model: {e}")
            self.chatbot = None
    
    def get_wellness_advice(self, stress_level: int, work_hours: int, breaks_taken: int, productivity: int):
        """Get personalized wellness advice using LLM"""
        
        if not self.chatbot:
            return self.get_fallback_advice(stress_level, work_hours)
        
        try:
            prompt = f"""
            Employee Wellness Analysis:
            - Current Stress Level: {stress_level}/10
            - Work Hours Today: {work_hours}
            - Breaks Taken: {breaks_taken}
            - Self-rated Productivity: {productivity}/10
            
            As an expert mental health and wellness coach, provide 3 practical, actionable recommendations to improve mental well-being and reduce stress. Focus on immediate, implementable strategies.
            
            Recommendations:
            1.
            """
            
            response = self.chatbot(
                prompt,
                max_length=250,
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True
            )
            
            return self.clean_response(response[0]['generated_text'])
            
        except Exception as e:
            logger.error(f"Error in LLM generation: {e}")
            return self.get_fallback_advice(stress_level, work_hours)
    
    def get_company_recommendations(self, department: str, avg_stress: float, attrition_rate: float):
        """Get company-level wellness recommendations"""
        
        if not self.chatbot:
            return self.get_fallback_company_recommendations(department, avg_stress)
        
        try:
            prompt = f"""
            Department Wellness Analysis:
            - Department: {department}
            - Average Stress Level: {avg_stress}/10
            - Attrition Rate: {attrition_rate}%
            
            As an HR and workplace wellness expert, provide 3 strategic recommendations to improve team mental health, reduce stress, and lower attrition. Focus on practical policies and cultural changes.
            
            Strategic Recommendations:
            1.
            """
            
            response = self.chatbot(
                prompt,
                max_length=300,
                num_return_sequences=1,
                temperature=0.6
            )
            
            return self.clean_response(response[0]['generated_text'])
            
        except Exception as e:
            logger.error(f"Error in company recommendations: {e}")
            return self.get_fallback_company_recommendations(department, avg_stress)
    
    def get_fallback_advice(self, stress_level: int, work_hours: int):
        """Fallback advice when LLM is not available"""
        advice = []
        
        if stress_level >= 8:
            advice.extend([
                "🚨 Take an immediate 15-minute break away from your screen",
                "💧 Drink water and do 2 minutes of deep breathing",
                "🚶 Take a short walk outside if possible"
            ])
        elif stress_level >= 5:
            advice.extend([
                "⏰ Schedule a proper lunch break away from your desk",
                "🎵 Listen to calming music for 10 minutes",
                "🧘 Try 5-minute desk stretches"
            ])
        else:
            advice.extend([
                "👍 Maintain your current healthy routine",
                "💪 Continue taking regular breaks",
                "🥗 Stay hydrated and eat nutritious meals"
            ])
        
        if work_hours > 9:
            advice.append("🕒 Consider setting stricter work hour boundaries")
        
        return "\n".join(advice)
    
    def get_fallback_company_recommendations(self, department: str, avg_stress: float):
        """Fallback company recommendations"""
        recommendations = []
        
        if avg_stress >= 7.0:
            recommendations.extend([
                "Implement mandatory break reminders for the team",
                "Provide stress management training workshops",
                "Consider flexible work hour options"
            ])
        else:
            recommendations.extend([
                "Continue current wellness initiatives",
                "Gather regular feedback from team members",
                "Promote work-life balance consistently"
            ])
        
        return "\n".join(recommendations)
    
    def clean_response(self, text: str):
        """Clean and format the LLM response"""
        # Remove the prompt part from response
        if "Recommendations:" in text:
            text = text.split("Recommendations:")[-1].strip()
        
        # Ensure proper formatting
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines[:6])  # Return max 6 lines

# Global instance
llm_engine = LLMEngine()
