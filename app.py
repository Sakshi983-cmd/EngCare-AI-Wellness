# app.py ke imports mein ye add karo
import requests
import json

# Backend URL setup function
def get_backend_url():
    return "http://localhost:8000"  # Local testing ke liye

# Stress analysis function add karo
def analyze_with_ai(stress_level, work_hours, breaks_taken, productivity):
    try:
        backend_url = get_backend_url()
        data = {
            "stress_level": stress_level,
            "work_hours": work_hours,
            "breaks_taken": breaks_taken,
            "productivity": productivity
        }
        response = requests.post(f"{backend_url}/analyze-stress", json=data)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except:
        return None

# Main function mein ye CHANGE karo:
if st.button("🎯 Get AI Recommendations"):
    with st.spinner("AI analyzing your wellness..."):
        # AI analysis call karo
        ai_result = analyze_with_ai(stress_level, work_hours, breaks_taken, 7)
        
        if ai_result:
            st.success(f"""
            🤖 **AI Wellness Analysis:**
            
            🎯 Stress Score: {ai_result.get('stress_analysis', {}).get('stress_score', 'N/A')}
            📊 Risk Level: {ai_result.get('stress_analysis', {}).get('risk_level', 'N/A')}
            
            💡 Recommendations:
            {ai_result.get('wellness_advice', 'Take a break and practice mindfulness.')}
            """)
        else:
            # Fallback recommendations
            st.success("""
            🤖 **AI Wellness Coach Recommendations:**
            1. Take a 15-minute walk break
            2. Practice 5-minute deep breathing  
            3. Hydrate - drink 2 glasses of water
            4. Do quick desk stretches
            """)
