import streamlit as st
import asyncio
import websockets
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import requests
import numpy as np
from typing import Dict, List, Optional
import base64
import random
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Import backend services
try:
    from stress_analyzer import StressAnalyzer
    from llm_engine import LLMEngine
except ImportError:
    # Fallback mock classes if imports fail
    class StressAnalyzer:
        def analyze_stress(self, text):
            stress_level = random.uniform(0.1, 0.8)
            return {
                "stress_level": stress_level,
                "confidence": 0.85,
                "level": "Low" if stress_level < 0.4 else "Moderate" if stress_level < 0.7 else "High",
                "recommendations": [
                    "Take a 5-minute break",
                    "Practice deep breathing",
                    "Listen to calming music"
                ]
            }
    
    class LLMEngine:
        def get_wellness_advice(self, problem):
            solutions = {
                "stress": "Try the 4-7-8 breathing technique: Inhale for 4 seconds, hold for 7, exhale for 8.",
                "burnout": "Take a complete digital detox for 2 hours. No screens, just relaxation.",
                "anxiety": "Practice grounding technique: Name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, 1 you can taste.",
                "focus": "Use the Pomodoro technique: 25 minutes focused work, 5 minutes break.",
                "sleep": "Avoid screens 1 hour before bed. Try reading a physical book.",
                "workload": "Break tasks into smaller chunks and prioritize using Eisenhower Matrix."
            }
            return solutions.get(problem.lower(), "Take a short walk and practice mindfulness.")

# Custom CSS and JS loader
def load_custom_assets():
    # Load CSS
    try:
        with open('assets/css/custom.css', 'r') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except:
        st.markdown("""
        <style>
        .main { background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%); color: white; }
        .glass-card { background: rgba(26,26,46,0.7); backdrop-filter: blur(20px); border-radius: 20px; padding: 20px; margin: 10px 0; }
        .stButton button { background: linear-gradient(135deg, #667eea, #764ba2); color: white; border: none; border-radius: 10px; }
        </style>
        """, unsafe_allow_html=True)
    
    # Load JavaScript
    try:
        with open('assets/js/animations.js', 'r') as f:
            st.markdown(f'<script>{f.read()}</script>', unsafe_allow_html=True)
    except:
        pass
    
    # Load particles.js and confetti from CDN
    st.markdown('''
        <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
        <div id="particles-js"></div>
        <script>
        particlesJS('particles-js', {
            particles: {
                number: { value: 80, density: { enable: true, value_area: 800 } },
                color: { value: "#667eea" },
                shape: { type: "circle" },
                opacity: { value: 0.5, random: true },
                size: { value: 3, random: true },
                line_linked: { enable: true, distance: 150, color: "#764ba2", opacity: 0.4, width: 1 },
                move: { enable: true, speed: 2, direction: "none", random: true }
            }
        });
        </script>
    ''', unsafe_allow_html=True)

def initialize_session_state():
    """Initialize all session state variables"""
    defaults = {
        'user_data': {
            'stress_level': 0.3,
            'wellness_points': 450,
            'level': 2,
            'achievements': ['First Step', 'Meditation Guru'],
            'streak': 5,
            'burnout_risk': 0.25,
            'mood': 'calm'
        },
        'problem_log': [],
        'solutions_given': [],
        'chat_history': [],
        'last_stress_update': datetime.now(),
        'ai_engine': LLMEngine(),
        'stress_analyzer': StressAnalyzer(),
        'real_time_data': {
            'stress_trend': [],
            'productivity': [],
            'mood_changes': []
        }
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def create_animated_stress_meter():
    """Create animated stress meter with real-time updates"""
    stress_level = st.session_state.user_data['stress_level']
    stress_color = "#00ff87" if stress_level < 0.4 else "#ff9966" if stress_level < 0.7 else "#ff4757"
    stress_text = "Low" if stress_level < 0.4 else "Moderate" if stress_level < 0.7 else "High"
    
    st.markdown(f"""
    <div class="glass-card">
        <h3>🧠 Real-time Stress Level</h3>
        <div class="stress-meter">
            <div class="stress-level" style="width: {stress_level * 100}%; background: linear-gradient(90deg, {stress_color}, #60efff);"></div>
        </div>
        <p style="text-align: center; margin-top: 10px; font-weight: bold; color: {stress_color};">
            {stress_level * 100:.1f}% - {stress_text}
        </p>
        <div style="text-align: center; font-size: 12px; color: #ccc;">
            Last updated: {st.session_state.last_stress_update.strftime('%H:%M:%S')}
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_problem_solver():
    """Main problem solver interface"""
    st.markdown("### 🎯 AI Problem Solver")
    
    # Problem categories
    problems = [
        "Work Stress & Pressure",
        "Burnout & Exhaustion", 
        "Anxiety & Overthinking",
        "Focus & Concentration Issues",
        "Sleep Problems",
        "Workload Management",
        "Team Conflicts",
        "Work-Life Balance",
        "Motivation Issues",
        "Time Management"
    ]
    
    selected_problem = st.selectbox("What's bothering you today?", problems)
    
    if st.button("Get AI Solution", key="solve_problem"):
        with st.spinner("🤔 Analyzing your problem..."):
            time.sleep(1.5)
            solution = st.session_state.ai_engine.get_wellness_advice(selected_problem)
            
            # Log the problem and solution
            st.session_state.problem_log.append({
                'problem': selected_problem,
                'solution': solution,
                'timestamp': datetime.now(),
                'stress_before': st.session_state.user_data['stress_level']
            })
            
            # Show solution in a beautiful card
            st.markdown(f"""
            <div class="glass-card" style="border-left: 4px solid #00ff87;">
                <h4>💡 AI Solution for '{selected_problem}'</h4>
                <p style="font-size: 16px; line-height: 1.6;">{solution}</p>
                <div style="margin-top: 15px; padding: 10px; background: rgba(0,255,135,0.1); border-radius: 10px;">
                    <strong>🎯 Quick Action:</strong> Try this immediately for relief
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Update user metrics
            st.session_state.user_data['wellness_points'] += 25
            st.session_state.user_data['stress_level'] = max(0.1, st.session_state.user_data['stress_level'] - 0.15)
            
            # Show confetti for successful solution
            st.markdown("""
            <script>
            confetti({
                particleCount: 100,
                spread: 70,
                origin: { y: 0.6 }
            });
            </script>
            """, unsafe_allow_html=True)
            
            st.success("✅ Solution applied! +25 Wellness Points")

def create_emergency_support():
    """Emergency/crisis support section"""
    st.markdown("### 🚨 Emergency Support")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🆘 Immediate Stress Relief", use_container_width=True):
            with st.spinner("Loading immediate relief techniques..."):
                time.sleep(1)
                st.markdown("""
                <div class="glass-card" style="border-left: 4px solid #ff4757;">
                    <h4>🚑 Immediate Stress Relief</h4>
                    <ol style="line-height: 2;">
                        <li><strong>Box Breathing:</strong> Inhale 4s → Hold 4s → Exhale 4s → Hold 4s</li>
                        <li><strong>5-4-3-2-1 Grounding:</strong> Name 5 things you see, 4 you feel, 3 you hear, 2 you smell, 1 you taste</li>
                        <li><strong>Cold Water:</strong> Splash cold water on your face</li>
                        <li><strong>Walk:</strong> Take a 2-minute walk away from your desk</li>
                    </ol>
                </div>
                """, unsafe_allow_html=True)
    
    with col2:
        if st.button("📞 Crisis Helpline", use_container_width=True):
            st.markdown("""
            <div class="glass-card">
                <h4>📞 Professional Support</h4>
                <p><strong>National Mental Health Helpline:</strong> 1-800-662-HELP</p>
                <p><strong>Crisis Text Line:</strong> Text HOME to 741741</p>
                <p><strong>Emergency:</strong> 911 or your local emergency number</p>
                <p><em>You're not alone. Professional help is available 24/7.</em></p>
            </div>
            """, unsafe_allow_html=True)

def create_wellness_dashboard():
    """Main wellness dashboard"""
    st.title("🧠 EngCare - AI Wellness Assistant")
    
    # Real-time stress meter
    create_animated_stress_meter()
    
    # Key metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="glass-card" style="text-align: center;">
            <h3>⭐ Level</h3>
            <h1 style="color: #667eea; margin: 0;">{st.session_state.user_data['level']}</h1>
            <p>Wellness Warrior</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="glass-card" style="text-align: center;">
            <h3>🔥 Streak</h3>
            <h1 style="color: #ff9966; margin: 0;">{st.session_state.user_data['streak']}</h1>
            <p>Days Active</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="glass-card" style="text-align: center;">
            <h3>🏆 Points</h3>
            <h1 style="color: #00ff87; margin: 0;">{st.session_state.user_data['wellness_points']}</h1>
            <p>Wellness Points</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        burnout_risk = st.session_state.user_data['burnout_risk']
        risk_color = "#00ff87" if burnout_risk < 0.3 else "#ff9966" if burnout_risk < 0.6 else "#ff4757"
        st.markdown(f"""
        <div class="glass-card" style="text-align: center;">
            <h3>🔮 Burnout Risk</h3>
            <h1 style="color: {risk_color}; margin: 0;">{burnout_risk * 100:.0f}%</h1>
            <p>7-Day Forecast</p>
        </div>
        """, unsafe_allow_html=True)

def create_ai_recommendations():
    """AI-powered personalized recommendations"""
    st.markdown("### 🤖 Your Wellness Assistant")
    
    stress_level = st.session_state.user_data['stress_level']
    
    if stress_level > 0.7:
        recommendations = [
            {"icon": "🧘", "title": "Guided Meditation", "duration": "10 min", "urgency": "high", "desc": "Calm your mind with breathing exercises"},
            {"icon": "🚶", "title": "Nature Walk", "duration": "15 min", "urgency": "high", "desc": "Connect with nature to reduce stress"},
            {"icon": "🎵", "title": "Calming Music", "duration": "5 min", "urgency": "medium", "desc": "Listen to relaxing sounds"}
        ]
    elif stress_level > 0.4:
        recommendations = [
            {"icon": "💪", "title": "Desk Stretches", "duration": "3 min", "urgency": "medium", "desc": "Release physical tension"},
            {"icon": "☕", "title": "Mindful Break", "duration": "5 min", "urgency": "medium", "desc": "Step away from screen"},
            {"icon": "📝", "title": "Journaling", "duration": "7 min", "urgency": "low", "desc": "Write down your thoughts"}
        ]
    else:
        recommendations = [
            {"icon": "🎯", "title": "Focus Session", "duration": "25 min", "urgency": "low", "desc": "Deep work with Pomodoro"},
            {"icon": "🏃", "title": "Quick Exercise", "duration": "5 min", "urgency": "low", "desc": "Boost energy levels"},
            {"icon": "📚", "title": "Learning", "duration": "15 min", "urgency": "low", "desc": "Develop new skills"}
        ]
    
    for rec in recommendations:
        urgency_color = "#ff4757" if rec["urgency"] == "high" else "#ff9966" if rec["urgency"] == "medium" else "#00ff87"
        
        st.markdown(f"""
        <div class="glass-card">
            <div style="display: flex; align-items: center; gap: 15px;">
                <div style="font-size: 2em;">{rec['icon']}</div>
                <div style="flex: 1;">
                    <h4 style="margin: 0;">{rec['title']}</h4>
                    <p style="margin: 5px 0; color: #ccc; font-size: 14px;">{rec['desc']}</p>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: #aaa;">⏱️ {rec['duration']}</span>
                        <span style="background: {urgency_color}; padding: 4px 12px; border-radius: 12px; font-size: 12px; color: white;">
                            {rec['urgency'].upper()}
                        </span>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def create_gamification_section():
    """Gamification and achievements"""
    st.markdown("### 🎮 Wellness Game")
    
    # Progress to next level
    current_points = st.session_state.user_data['wellness_points']
    next_level_points = st.session_state.user_data['level'] * 1000
    progress = min(current_points / next_level_points, 1.0)
    
    st.markdown(f"""
    <div class="glass-card">
        <h4>Level Progress</h4>
        <div style="width: 100%; background: rgba(255, 255, 255, 0.1); border-radius: 10px; overflow: hidden;">
            <div style="width: {progress * 100}%; background: linear-gradient(90deg, #667eea, #764ba2); height: 12px; border-radius: 10px; transition: all 0.5s ease;"></div>
        </div>
        <p style="text-align: center; margin: 10px 0; color: #ccc;">
            {current_points} / {next_level_points} points to level {st.session_state.user_data['level'] + 1}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Achievements
    st.markdown("#### 🏆 Your Achievements")
    achievements = [
        {"name": "First Step", "earned": True, "icon": "🚶", "desc": "Completed first session"},
        {"name": "7-Day Streak", "earned": st.session_state.user_data['streak'] >= 7, "icon": "🔥", "desc": "7 consecutive days"},
        {"name": "Stress Master", "earned": st.session_state.user_data['stress_level'] < 0.3, "icon": "🧠", "desc": "Low stress maintained"},
        {"name": "Problem Solver", "earned": len(st.session_state.problem_log) > 5, "icon": "💡", "desc": "5+ problems solved"},
    ]
    
    cols = st.columns(4)
    for idx, achievement in enumerate(achievements):
        with cols[idx]:
            opacity = "1" if achievement["earned"] else "0.3"
            st.markdown(f"""
            <div style="text-align: center; opacity: {opacity}; padding: 10px;">
                <div style="font-size: 2.5em; margin-bottom: 5px;">{achievement['icon']}</div>
                <p style="font-weight: bold; margin: 5px 0; font-size: 12px;">{achievement['name']}</p>
                <p style="font-size: 10px; color: #ccc; margin: 0;">{achievement['desc']}</p>
            </div>
            """, unsafe_allow_html=True)

def create_analytics_dashboard():
    """Advanced analytics and insights"""
    st.markdown("### 📊 Your Wellness Analytics")
    
    # Generate sample analytics data
    dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='D')
    stress_data = [max(0.1, min(0.9, 0.5 + 0.3 * np.sin(i/3) + random.uniform(-0.2, 0.2))) for i in range(len(dates))]
    productivity_data = [1 - stress + random.uniform(-0.1, 0.1) for stress in stress_data]
    
    # Create interactive chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=dates, y=stress_data,
        mode='lines+markers',
        name='Stress Level',
        line=dict(color='#ff4757', width=3),
        fill='tozeroy',
        opacity=0.6
    ))
    
    fig.add_trace(go.Scatter(
        x=dates, y=productivity_data,
        mode='lines+markers',
        name='Productivity',
        line=dict(color='#00ff87', width=3),
        fill='tozeroy',
        opacity=0.6
    ))
    
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=300,
        showlegend=True,
        margin=dict(l=0, r=0, t=30, b=0)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Insights
    avg_stress = np.mean(stress_data[-7:])  # Last 7 days
    insight = ""
    if avg_stress < 0.4:
        insight = "🎉 Excellent! Your stress levels are well managed."
    elif avg_stress < 0.6:
        insight = "👍 Good job! You're maintaining healthy stress levels."
    else:
        insight = "💡 Consider using our problem solver for stress relief techniques."
    
    st.info(insight)

def simulate_real_time_updates():
    """Simulate real-time data updates"""
    current_time = datetime.now()
    if (current_time - st.session_state.last_stress_update).seconds > 10:  # Update every 10 seconds
        # Small random fluctuations in stress
        change = random.uniform(-0.05, 0.05)
        st.session_state.user_data['stress_level'] = max(0.1, min(0.9, 
            st.session_state.user_data['stress_level'] + change))
        
        # Update burnout risk based on stress trend
        if st.session_state.user_data['stress_level'] > 0.6:
            st.session_state.user_data['burnout_risk'] = min(0.9, 
                st.session_state.user_data['burnout_risk'] + 0.02)
        else:
            st.session_state.user_data['burnout_risk'] = max(0.1, 
                st.session_state.user_data['burnout_risk'] - 0.01)
        
        st.session_state.last_stress_update = current_time

def main():
    # Configure page
    st.set_page_config(
        page_title="EngCare - AI Wellness Platform",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Load custom assets
    load_custom_assets()
    
    # Initialize session state
    initialize_session_state()
    
    # Simulate real-time updates
    simulate_real_time_updates()
    
    # Main app layout
    create_wellness_dashboard()
    
    # Emergency support at the top for quick access
    create_emergency_support()
    
    # Two column layout for main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        create_problem_solver()
        create_analytics_dashboard()
        
        # Problem history
        if st.session_state.problem_log:
            st.markdown("### 📝 Recent Solutions")
            for i, log in enumerate(list(reversed(st.session_state.problem_log))[-3:]):
                st.markdown(f"""
                <div class="glass-card" style="margin: 10px 0; padding: 15px;">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div>
                            <strong>{log['problem']}</strong>
                            <p style="margin: 5px 0; color: #ccc; font-size: 14px;">{log['solution'][:100]}...</p>
                        </div>
                        <span style="color: #aaa; font-size: 12px;">{log['timestamp'].strftime('%H:%M')}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    with col2:
        create_ai_recommendations()
        create_gamification_section()
        
        # Quick stress check
        st.markdown("### 😊 Quick Check-in")
        mood = st.selectbox("How are you feeling?", ["😊 Great", "😐 Okay", "😟 Stressed", "😴 Tired", "🔥 Energized"])
        
        if st.button("Update Mood", use_container_width=True):
            st.session_state.user_data['mood'] = mood
            st.session_state.user_data['wellness_points'] += 10
            st.success("Mood updated! +10 points")
            
            st.markdown("""
            <script>
            confetti({
                particleCount: 50,
                spread: 50,
                origin: { y: 0.6 }
            });
            </script>
            """, unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666; font-size: 12px;'>"
        "🧠 EngCare AI Wellness Platform • Your mental health matters • Confidential & Secure"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
