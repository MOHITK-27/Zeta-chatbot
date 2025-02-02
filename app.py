import streamlit as st
from groq import Groq
import time
import random
import re
from pr import PERSONALITY_TRAITS, PREDEFINED_RESPONSES

# Initialize Groq client
try:
    client = Groq(api_key=st.secrets.get("GROQ_API_KEY"))
except Exception as e:
    st.error(f"Error initializing Groq client: {str(e)}")
    st.stop()

# App configuration
st.set_page_config(page_title="ZETA", page_icon="🤖", layout="wide")

# ======================================
# Custom CSS
# ======================================
st.markdown("""
<style>
    .stApp {
        max-width: 12000px;
        margin: 0 auto;
    }
    
    [data-testid="stChatMessage"] {
        padding: 1.5rem;
        border-radius: 0.75rem;
        margin: 1rem 0;
        background-color: #f8f9fa;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .thinking-block {
        font-family: 'Courier New', monospace;
        color: #666666;
        border-left: 3px solid #4a90e2;
        margin: 10px 0;
        padding: 10px 15px;
        background-color: #f8f9fa;
        border-radius: 5px;
        white-space: pre-wrap;
    }
    
    .thinking-block::before {
        content: "Thinking Process:";
        display: block;
        font-weight: bold;
        margin-bottom: 8px;
        color: #333333;
    }
    
    .user-message {
        border-left: 4px solid #4a90e2;
    }
    
    .assistant-message {
        border-right: 4px solid #4a90e2;
    }
</style>
""", unsafe_allow_html=True)

# ======================================
# Response Processing
# ======================================
def get_predefined_response(user_input):
    user_input = user_input.lower()
    for category, data in PREDEFINED_RESPONSES.items():
        for pattern in data["patterns"]:
            if re.search(pattern, user_input, re.IGNORECASE):
                return random.choice(data["responses"])
    return None

def process_think_blocks(response):
    processed_response = re.sub(
        r'<think>(.*?)</think>',
        r'<div class="thinking-block">\1</div>',
        response,
        flags=re.DOTALL
    )
    return processed_response

# ======================================
# Sidebar Configuration
# ======================================
def display_sidebar():
    with st.sidebar:
        st.title("⚙️ Settings")
        
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
        
        st.divider()
        
        # Fun Section
        st.header("🎉 Fun")
        f1, f2 = st.columns([1,1])
        with f1:
            if st.button("🎊 Confetti"):
                st.balloons()
        with f2:
            if st.button("❄️ Snow"):
                st.snow()
        
        if st.button("🤯 Random Fact"):
            facts = [
                "First computer virus: Creeper (1971)",
                "HTTP was created in 1989 at CERN",
                "Qwerty layout slows typing to prevent jams"
            ]
            st.toast(random.choice(facts), icon="💡")

# ======================================
# Main App
# ======================================
def main():
    st.title("🤖 ZETA")
    st.caption("Your Intelligent Assistant Made by Mohit")
    st.divider()

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display sidebar
    display_sidebar()
    st.sidebar.title("Chat history")
    st.sidebar.warning("In development")
    # Display chat messages
    for message in st.session_state.messages:
        avatar = "👤" if message["role"] == "user" else "🤖"
        with st.chat_message(message["role"], avatar=avatar):
            if message["role"] == "assistant":
                processed_content = process_think_blocks(message["content"])
                st.markdown(processed_content, unsafe_allow_html=True)
            else:
                st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("How can I help you today?"):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant", avatar="🤖"):
            response_placeholder = st.empty()
            full_response = ""
            
            try:
                # Check for predefined response
                predefined = get_predefined_response(prompt)
                
                if predefined:
                    prefix = random.choice(PERSONALITY_TRAITS["catchphrases"])
                    response = f"{prefix} {predefined}"
                    full_response = response
                    response_placeholder.markdown(response)
                else:
                    messages = [{"role": m["role"], "content": m["content"]} 
                              for m in st.session_state.messages]
                    
                    completion = client.chat.completions.create(
                        model=st.session_state.default_model,
                        messages=messages,
                        stream=True,
                        temperature=0.7,
                        max_tokens=1024
                    )
                    
                    # Stream response
                    for chunk in completion:
                        chunk_content = chunk.choices[0].delta.content or ""
                        full_response += chunk_content
                        response_placeholder.markdown(full_response + "▌")
                    
                    # Process think blocks
                    processed_response = process_think_blocks(full_response)
                    response_placeholder.markdown(processed_response, unsafe_allow_html=True)

            except Exception as e:
                error_jokes = [
                    "Oops! My logic gates got stuck! 🔌",
                    "Error detected: Human input too interesting!",
                    "My brain did a segfault... try again?",
                ]
                full_response = f"⚠️ **Error:** {str(e)}\n\n{random.choice(error_jokes)}"
                response_placeholder.markdown(full_response)
            
            # Add to history
            st.session_state.messages.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    main()