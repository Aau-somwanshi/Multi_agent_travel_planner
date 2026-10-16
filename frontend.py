import os
import json
import streamlit as st
from datetime import datetime
from langchain_core.messages import HumanMessage
from main import app

# Page configuration
st.set_page_config(
    page_title="VoyageAI | Autonomous Travel Planner", 
    page_icon="✈️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Cyberpunk Glassmorphism CSS injection
st.markdown("""
    <style>
    /* Global App Background */
    .stApp {
        background-color: #090D16;
        background-image: 
            radial-gradient(at 0% 0%, rgba(121, 40, 202, 0.15) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(0, 242, 254, 0.12) 0px, transparent 50%);
        color: #F8FAFC;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(11, 15, 25, 0.95);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }

    /* Title Styling */
    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #00F2FE 0%, #4FACFE 50%, #00F2FE 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .hero-subtitle {
        font-size: 1rem;
        color: #94A3B8;
        margin-bottom: 20px;
    }

    /* Glowing Action Button */
    div.stButton > button {
        background: linear-gradient(135deg, #00F2FE 0%, #4FACFE 100%);
        color: #000000;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 1.2rem;
        font-weight: 700;
        transition: all 0.3s ease;
        box-shadow: 0 0 20px rgba(0, 242, 254, 0.4);
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 30px rgba(0, 242, 254, 0.7);
    }

    /* Status Container Styling */
    div[data-testid="stStatus"] {
        background-color: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(0, 242, 254, 0.3);
        border-radius: 12px;
    }

    /* Agent Badge Tags */
    .agent-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        background: rgba(0, 242, 254, 0.1);
        color: #00F2FE;
        border: 1px solid rgba(0, 242, 254, 0.2);
        margin-right: 5px;
        margin-bottom: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Chat session initialization
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar Controls
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1488646953014-85cb44e25828?auto=format&fit=crop&w=600&q=80", width="stretch")
    st.markdown("### 🧭 Journey Parameters")
    
    travel_style = st.selectbox(
        "Preferred Style", 
        ["Luxury & Leisure", "Budget Backpacker", "Adventure & Trekking", "Cultural Explorer"]
    )
    budget_range = st.slider("Estimated Budget (₹)", 5000, 150000, 35000, step=5000)
    
    st.markdown("---")
    
    # Export / Download Section in Sidebar
    st.markdown("### 📥 Report Export")
    assistant_messages = [msg for msg in st.session_state.chat_history if msg["role"] == "assistant"]
    
    if assistant_messages:
        latest_report = assistant_messages[-1]
        report_data = f"""==================================================
VOYAGEAI - MULTI-AGENT TRAVEL PLANNING REPORT
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
==================================================

[FINAL ITINERARY PLAN]
{latest_report['content']}

--------------------------------------------------
[RAW FLIGHT TOOL DATA]
{latest_report.get('flight_data', 'N/A')}

--------------------------------------------------
[RAW HOTEL TOOL DATA]
{latest_report.get('hotel_data', 'N/A')}
==================================================
"""
        st.download_button(
            label="📥 Download Full Report (.txt)",
            data=report_data,
            file_name=f"VoyageAI_Itinerary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    else:
        st.info("Generate a travel plan in chat to enable downloading the report.")

    st.markdown("---")
    st.markdown("### 🤖 Active LangGraph Nodes")
    st.markdown("""
    <div>
        <span class="agent-badge">✈️ Flight Agent</span>
        <span class="agent-badge">🏨 Hotel Agent</span>
        <span class="agent-badge">🗓️ Itinerary Agent</span>
        <span class="agent-badge">📋 Final Synthesizer</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("🧹 Clear Chat History", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

# Main Canvas Header
st.markdown('<p class="hero-title">🌍 VoyageAI Agentic Dashboard</p>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">Multi-Agent LangGraph System Powered by Real-Time Data & Groq LLM Engine</p>', unsafe_allow_html=True)

# LangGraph Config Thread
config = {
    "configurable": {
        "thread_id": "user_aarohi"
    }
}

# Display previous conversation history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"], avatar="🤖" if message["role"] == "assistant" else "👤"):
        st.markdown(message["content"])
        if message["role"] == "assistant" and "flight_data" in message:
            tab1, tab2 = st.tabs(["✈️ Flight Tool Raw Data", "🏨 Hotel Tool Raw Data"])
            with tab1:
                st.code(message["flight_data"], language="text")
            with tab2:
                st.code(message["hotel_data"], language="text")

# Chat input prompt widget
if user_query := st.chat_input("Where would you like to travel? (e.g., Plan a 3 day trip from Pune to Goa)"):
    
    # Bundle user choices into the input prompt
    enhanced_query = f"{user_query} | Preferred Style: {travel_style} | Budget: ₹{budget_range}"
    
    # Render user query
    st.session_state.chat_history.append({"role": "user", "content": user_query})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_query)

    # Render assistant agent processing
    with st.chat_message("assistant", avatar="🤖"):
        with st.status("🚀 LangGraph Pipeline Executing...", expanded=True) as status:
            st.write("✈️ **Flight Agent**: Fetching flight schedules via AviationStack...")
            st.write("🏨 **Hotel Agent**: Scraping accommodation options via Tavily...")
            st.write("🗓️ **Itinerary Agent**: Synthesizing day-by-day plan using Groq LLM...")
            
            try:
                # Invoke your compiled Python LangGraph app from main.py
                result = app.invoke(
                    {
                        "messages": [HumanMessage(content=enhanced_query)],
                        "user_query": enhanced_query,
                        "flight_results": "",
                        "hotel_results": "",
                        "itinerary": "",
                        "llm_calls": 0
                    },
                    config=config
                )
                
                status.update(label="✨ Travel Plan Generated Successfully!", state="complete", expanded=False)
                
            except Exception as e:
                status.update(label="❌ Agent Execution Failed", state="error", expanded=True)
                st.error(f"Error Details: `{e}`")
                result = None

        if result:
            final_response = result["messages"][-1].content
            flight_res = result.get("flight_results", "No flight data captured.")
            hotel_res = result.get("hotel_results", "No hotel data captured.")
            
            # Display final generated output
            st.markdown(final_response)
            
            # Expandable Raw Data Tabs
            tab1, tab2 = st.tabs(["✈️ Flight Tool Raw Data", "🏨 Hotel Tool Raw Data"])
            with tab1:
                st.code(flight_res, language="text")
            with tab2:
                st.code(hotel_res, language="text")
            
            # Save message to session state
            st.session_state.chat_history.append({
                "role": "assistant", 
                "content": final_response,
                "flight_data": flight_res,
                "hotel_data": hotel_res
            })
            
            # Rerun immediately so the download button updates right away
            st.rerun()