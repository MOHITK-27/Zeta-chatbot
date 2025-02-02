import streamlit as st
import time
import random
from utilities import file_analyzer

def show_sidebar():
    with st.sidebar:
        st.title("⚙️ Dashboard")
        st.metric("Total Messages", len(st.session_state.messages))
        
        # Model Selection
        st.header("🧠 AI Model")
        model_options = {
            "DeepSeek R1": "deepseek-r1-distill-llama-70b",
            "Mixtral 8x7B": "mixtral-8x7b-32768", 
            "Llama2 70B": "llama2-70b-4096"
        }
        selected_model = st.selectbox(
            "Select Model",
            options=list(model_options.keys()),
            index=0,
            label_visibility="collapsed"
        )
        st.session_state.default_model = model_options[selected_model]
        
        st.divider()

        # Chat Controls
        st.header("💬 Chat")
        cc1, cc2 = st.columns([1,1])
        with cc1:
            if st.button("🧹 New Chat", help="Start fresh conversation"):
                st.session_state.messages = []
                st.rerun()
        with cc2:
            if st.button("📥 Export", help="Save chat history"):
                chat_history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages])
                st.download_button("Download", chat_history, file_name="chat_history.txt")
        
        # File Analyzer
        analysis_result = file_analyzer()
        if analysis_result:
            st.info(analysis_result)
        
        st.divider()
        
        # Fun Section
        st.header("🎉 Features")
        show_fun_controls()

def show_fun_controls():
    f1, f2 = st.columns([1,1])
    with f1:
        if st.button("🎊 Confetti"):
            st.balloons()
    with f2:
        if st.button("❄️ Snow"):
            st.snow()
    
    if st.button("🤯 Random Fact"):
        show_random_fact()

def show_random_fact():
    facts = [
        "First computer virus: Creeper (1971)",
        "HTTP was created in 1989 at CERN",
        "Qwerty layout slows typing to prevent jams"
    ]
    st.toast(random.choice(facts), icon="💡")