import streamlit as st
from groq import Groq
import time
import random
from ui import get_css, typing_animation, message_reactions, setup_header
from chat_manager import get_predefined_response, process_think_blocks, format_response
from utilities import web_search
from sidebar import show_sidebar

# Initialize Groq client
try:
    client = Groq(api_key=st.secrets.get("GROQ_API_KEY"))
except Exception as e:
    st.error(f"Error initializing Groq client: {str(e)}")
    st.stop()

# App configuration
st.set_page_config(page_title="ZETA", page_icon="🤖", layout="wide")
st.markdown(get_css(), unsafe_allow_html=True)

def main():
    # Setup modern header
    setup_header()
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display sidebar with controls
    show_sidebar()

    # Display chat messages with enhanced styling
    for i, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"], 
                           avatar="👤" if message["role"] == "user" else "🤖"):
            content = process_think_blocks(message["content"])
            st.markdown(f'<div class="{"user" if message["role"] == "user" else "assistant"}-message">{content}</div>', 
                      unsafe_allow_html=True)
            if message["role"] == "assistant":
                message_reactions(i)

    # Chat input handling
    if prompt := st.chat_input("How can I help you today?"):
        handle_user_input(prompt)

def handle_user_input(prompt):
    # Immediately display user message
    with st.chat_message("user", avatar="👤"):
        st.markdown(f'<div class="user-message">{prompt}</div>', unsafe_allow_html=True)
    
    # Add to session state after display
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Generate response
    with st.chat_message("assistant", avatar="🤖"):
        response_placeholder = st.empty()
        full_response = ""
        
        try:
            predefined = get_predefined_response(prompt)
            
            if predefined:
                full_response = format_response(predefined)
                response_placeholder.markdown(f'<div class="assistant-message">{full_response}</div>', 
                                            unsafe_allow_html=True)
            else:
                full_response = handle_ai_response(prompt, response_placeholder)
                
        except Exception as e:
            full_response = handle_error(e, response_placeholder)
            
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
def handle_ai_response(prompt, response_placeholder):
    messages = [{"role": m["role"], "content": m["content"]} 
               for m in st.session_state.messages]
    
    # Add web search context if needed
    if "search" in prompt.lower():
        messages.append({"role": "user", "content": f"{prompt}\n{web_search(prompt)}"})
    
    # Stream response from Groq API
    response_placeholder.markdown(typing_animation(), unsafe_allow_html=True)
    completion = client.chat.completions.create(
        model=st.session_state.default_model,
        messages=messages,
        stream=True,
        temperature=0.7,
        max_tokens=1024
    )
    
    full_response = stream_response(completion, response_placeholder)
    processed_response = f'<div class="assistant-message">{process_think_blocks(full_response)}</div>'
    response_placeholder.markdown(processed_response, unsafe_allow_html=True)
    return full_response

def stream_response(completion, response_placeholder):
    full_response = ""
    for chunk in completion:
        chunk_content = chunk.choices[0].delta.content or ""
        full_response += chunk_content
        response_placeholder.markdown(
            f'<div class="assistant-message">{full_response}▌</div>',
            unsafe_allow_html=True
        )
    return full_response

def handle_error(error, response_placeholder):
    error_jokes = [
        "Oops! My logic gates got stuck! 🔌",
        "Error detected: Human input too interesting!",
        "My brain did a segfault... try again?",
    ]
    error_msg = f"⚠️ **Error:** {str(error)}\n\n{random.choice(error_jokes)}"
    response_placeholder.markdown(
        f'<div class="assistant-message">{error_msg}</div>',
        unsafe_allow_html=True
    )
    return error_msg

if __name__ == "__main__":
    main()