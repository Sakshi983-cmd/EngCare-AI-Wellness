import streamlit as st
import requests
import json
import time
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="EngCare - AI Wellness Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    try:
        with open("assets/css/custom.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except:
        st.markdown("""
        <style>
        .stApp { background: #0E1117; color: white; }
        </style>
        """, unsafe_allow_html=True)

load_css()

# Main app
def main():
    st.markdown("""
    <div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; margin-bottom: 2rem;'>
        <h1>🛡️ EngCare</h1>
        <p>AI-Powered Engineer Wellness Platform</p>
    </div>
    """, unsafe_allow_html=True)

    # Stress tracking section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🧠 Your Mental Wellness")
        stress_level = st.slider("Current Stress Level (1-10)", 1, 10, 5)
        work_hours = st.number_input("Work Hours Today", 1, 16, 8)
        breaks_taken = st.number_input("Breaks Taken", 0, 10, 2)
        
        if st.button("🎯 Get AI Recommendations"):
            with st.spinner("AI analyzing your wellness..."):
                time.sleep(2)
                st.success("""
                🤖 **AI Wellness Coach Recommendations:**
                1. Take a 15-minute walk break
                2. Practice 5-minute deep breathing
                3. Hydrate - drink 2 glasses of water
                """)

    with col2:
        st.subheader("📊 Your Wellness Stats")
        st.metric("Wellness Score", "75/100", "+5")
        st.metric("Current Streak", "7 days", "🔥")
        st.metric("Team Rank", "#3", "↑2")

if __name__ == "__main__":
    main()
