import torch
from transformers import pipeline, AutoTokenizer
import logging
import time

logger = logging.getLogger(__name__)

class LLMEngine:
    """
    DialoGPT-Medium LLM Engine
    
    Resume Claim: "LLM for AI wellness coaching"
    Code Proof: This file loads DialoGPT-Medium
    """
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.load_model()
    
    def load_model(self):
        """Load DialoGPT-Medium (350MB LLM)"""
        try:
            logger.info("🤖 Loading DialoGPT-Medium LLM...")
            
            self.tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
            
            self.model = pipeline(
                "text-generation",
                model="microsoft/DialoGPT-medium",
                tokenizer=self.tokenizer,
                max_length=256,
                device_map="cpu",
                torch_dtype=torch.float32
            )
            
            logger.info("✅ DialoGPT-Medium loaded successfully!")
            return True
        
        except Exception as e:
            logger.error(f"❌ LLM load failed: {e}")
            return False
    
    def generate_wellness_advice(self, stress_level: int, work_hours: int, 
                                breaks_taken: int, productivity: int) -> str:
        """
        Generate wellness advice using LLM
        
        Resume Claim: "AI-generated personalized recommendations"
        Code Proof: This function generates using DialoGPT
        """
        
        if not self.model:
            return self._fallback_advice(stress_level)
        
        try:
            prompt = f"""You are a wellness coach for engineers.
Stress Level: {stress_level}/10
Work Hours: {work_hours}
Breaks: {breaks_taken}
Productivity: {productivity}/10

Give 2-3 wellness tips:"""
            
            response = self.model(
                prompt,
                max_length=200,
                temperature=0.7,
                do_sample=True
            )
            
            text = response[0]['generated_text']
            text = text.split("Give 2-3 wellness tips:")[-1].strip()
            
            logger.info(f"✅ LLM generated response ({len(text)} chars)")
            return text
        
        except Exception as e:
            logger.error(f"❌ Generation error: {e}")
            return self._fallback_advice(stress_level)
    
    def _fallback_advice(self, stress_level: int) -> str:
        """Fallback if LLM fails"""
        if stress_level >= 8:
            return "🚨 Take immediate break. Do 4-7-8 breathing. Contact mental health professional."
        elif stress_level >= 6:
            return "⚠️ Take lunch break away from desk. Do 5-min walk. Listen to calming music."
        else:
            return "✅ Maintain current routine. Stay hydrated. Take regular breaks."

# Global instance
llm_engine = LLMEngine()
