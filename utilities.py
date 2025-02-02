import streamlit as st
from googlesearch import search
from PyPDF2 import PdfReader
from PIL import Image

def web_search(query):
    try:
        results = list(search(query, num=3, stop=3, pause=1))
        return f"**Web Results:**\n- " + "\n- ".join(results)
    except Exception as e:
        return f"🔍 Web search unavailable: {str(e)}"

def file_analyzer():
    uploaded_file = st.sidebar.file_uploader(
        "📁 Upload File (PDF/Image/Text)",
        type=["pdf", "png", "jpg", "txt"]
    )
    
    if not uploaded_file:
        return ""
    
    file_type = uploaded_file.type
    if "pdf" in file_type:
        return analyze_pdf(uploaded_file)
    elif "image" in file_type:
        return analyze_image(uploaded_file)
    elif "text" in file_type:
        return analyze_text(uploaded_file)
    return ""

def analyze_pdf(file):
    reader = PdfReader(file)
    analysis = "\n".join([page.extract_text() for page in reader.pages[:3]])
    return f"**PDF Summary:**\n{analysis[:500]}..."

def analyze_image(file):
    img = Image.open(file)
    return f"**Image Analysis:** {img.size} pixels, {img.mode} mode"

def analyze_text(file):
    return f"**Text Content:**\n{file.getvalue().decode()[:500]}..."