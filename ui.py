# ui.py
import streamlit as st

def get_css():
    return """
    <style>
        :root {
            --primary: #4a90e2;
            --background: #d6e9ff;
            --text: #333333;
            --card-bg: #d1eaed;
            --user-bg: #A5BFCC;
            --assistant-bg: #A5BFCC;
        }
        
        [data-theme="dark"] {
            --primary: #7fb6ff;
            --background: #d6e9ff;
            --text: #333333;
            --card-bg: #d1eaed;
            --user-bg: #A5BFCC;
            --assistant-bg: #A5BFCC;
        }

        .stApp {
            max-width: 12000px;
            margin: 0 auto;
            background-color: var(--background) !important;
            color: var(--text) !important;
        }
        
        [data-testid="stChatMessage"] {
            padding: 1.5rem;
            border-radius: 15px;
            margin: 1.5rem 0;
            background-color: var(--card-bg) !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            animation: fadeIn 0.3s ease-out;
            transition: all 0.2s;
            border: none !important;
        }
        
        [data-testid="stChatMessage"].user-message {
            background-color: var(--user-bg) !important;
            margin-left: 20%;
        }
        
        [data-testid="stChatMessage"].assistant-message {
            background-color: var(--assistant-bg) !important;
            margin-right: 20%;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .thinking-block {
            background-color: rgba(252, 197, 250, 0.2) !important;
            font-family: 'Courier New', monospace;
            color: var(--text) !important;
            margin: 15px 0;
            padding: 15px;
            border-radius: 8px;
            white-space: pre-wrap;
            font-size: 0.9em;
        }
        
        .thinking-block::before {
            content: "🧠 Thinking Process:";
            display: block;
            font-weight: bold;
            margin-bottom: 10px;
            color: var(--primary) !important;
        }
        
        .typing-indicator {
            display: inline-flex;
            align-items: center;
            padding: 10px 20px;
            background: var(--card-bg) !important;
            border-radius: 25px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .typing-dot {
            width: 8px;
            height: 8px;
            margin: 0 3px;
            background: var(--primary) !important;
            border-radius: 50%;
            animation: bounce 1.4s infinite;
        }
        
        @keyframes bounce {
            0%, 80%, 100% { transform: translateY(0); }
            40% { transform: translateY(-8px); }
        }
        
        .st-emotion-cache-16txtl3 {
            background-color: var(--background) !important;
        }
        
        .stChatMessageContainer {
            background-color: transparent !important;
        }
        
        .header {
            background: linear-gradient(135deg, var(--primary) 0%, #4CAF50 100%);
            color: white;
            padding: 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
        }
    </style>
    """

def message_reactions(message_id):
    """Simplified reactions with feedback"""
    if f"reactions_{message_id}" not in st.session_state:
        st.session_state[f"reactions_{message_id}"] = {"👍": 0, "👎": 0}
    
    cols = st.columns(6)
    with cols[0]:
        if st.button("👍", key=f"like_{message_id}", help="Like this response"):
            st.session_state[f"reactions_{message_id}"]["👍"] += 1
            st.toast("Thanks for the feedback! ❤️")
    with cols[1]:
        if st.button("👎", key=f"dislike_{message_id}", help="Dislike this response"):
            st.session_state[f"reactions_{message_id}"]["👎"] += 1
            st.toast("Thanks for the feedback! ❤️")

def typing_animation():
    return """
    <div class="typing-indicator">
        <div class="typing-dot" style="animation-delay: 0s"></div>
        <div class="typing-dot" style="animation-delay: 0.2s"></div>
        <div class="typing-dot" style="animation-delay: 0.4s"></div>
    </div>
    """

def setup_header():
    st.markdown("""
    <div class="header">
        <h1>🤖 ZETA</h1>
        <p>Your Intelligent Assistant Made with ❤️ by Mohit</p>
    </div>
    """, unsafe_allow_html=True)