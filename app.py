import os
import io
import streamlit as st
from summarizer import extract_article, generate_summary, extract_from_pdf, extract_from_image

# 1. Performance Optimizations
# Set environment variables for better performance in containerized environments
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OMP_NUM_THREADS"] = "1"

# 2. Page Configuration
st.set_page_config(
    page_title="NewsLens - AI News Summarizer",
    page_icon="🔍",
    layout="centered"
)

# Custom CSS for Rich Aesthetics (Glassmorphism & Gradients)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    .main {
        background-color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f0f4f8 0%, #e2e8f0 100%);
    }

    .title-text {
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        color: #1e293b;
        margin-bottom: 0.5rem;
        letter-spacing: -0.025em;
        background: linear-gradient(90deg, #2563eb, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .subtitle-text {
        font-size: 1.25rem;
        text-align: center;
        color: #334155; /* Darker than #64748b */
        margin-bottom: 2.5rem;
        font-weight: 500;
    }


    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #2563eb, #1d4ed8);
        color: white;
        border-radius: 12px;
        padding: 0.75rem;
        font-weight: 600;
        border: none;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        filter: brightness(1.1);
    }

    .summary-card {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(12px);
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-left: 8px solid #2563eb;
        margin-top: 2rem;
    }

    .summary-title {
        color: #2563eb;
        font-size: 1.75rem;
        font-weight: 800;
        margin-bottom: 1.25rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .summary-content {
        font-size: 1.15rem;
        line-height: 1.8;
        color: #1e293b;
    }

    div[data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.4);
        border: 1px solid rgba(0, 0, 0, 0.1);
        border-radius: 12px;
        margin-top: 1.5rem;
    }

    div[data-testid="stExpander"] p, div[data-testid="stExpander"] div {
        color: #1e293b !important; /* Force high contrast dark text */
    }
</style>

""", unsafe_allow_html=True)

@st.cache_resource
def load_summarizer():
    """Loads the summarization pipeline and caches it to avoid reloading."""
    from transformers import pipeline
    # facebook/bart-large-cnn is standard for high-quality news summaries
    return pipeline("summarization", model="facebook/bart-large-cnn")

# UI Header
st.markdown('<h1 class="title-text">NewsLens</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">Concise AI summarization for news articles and documents.</p>', unsafe_allow_html=True)

# Main Input Section
tab1, tab2 = st.tabs(["🔗 Paste URL", "📁 Upload Document"])

summary = ""
original_text = ""
original_title = "Uploaded Content"
error = None
url = None

with tab1:
    url_input = st.text_input("Article URL", placeholder="https://www.nytimes.com/...")
    if st.button("Generate Summary", key="url_btn"):
        if url_input:
            with st.spinner("🔍 Extracting article content..."):
                article_data = extract_article(url_input)
                if article_data['error']:
                    error = article_data['error']
                else:
                    original_text = article_data['text']
                    original_title = article_data['title']
                    url = url_input
        else:
            st.warning("Please provide a valid URL first.")

with tab2:
    uploaded_file = st.file_uploader("Upload PDF or Image", type=['pdf', 'png', 'jpg', 'jpeg'])
    if st.button("Summarize Upload", key="file_btn"):
        if uploaded_file is not None:
            with st.spinner("📄 Reading document..."):
                file_bytes = io.BytesIO(uploaded_file.read())
                if uploaded_file.name.lower().endswith('.pdf'):
                    original_text = extract_from_pdf(file_bytes)
                elif uploaded_file.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                    original_text = extract_from_image(file_bytes)
                
                if original_text.startswith("Error"):
                    error = original_text
                else:
                    original_title = uploaded_file.name
        else:
            st.warning("Please upload a file to summarize.")

# Execution and Results
if error:
    st.error(f"Analysis Failed: {error}")

if original_text and not error:
    with st.spinner("🤖 AI is analyzing the text..."):
        summarizer_model = load_summarizer()
        summary = generate_summary(original_text, summarizer_model)
        
    if summary:
        st.markdown(f"""
        <div class="summary-card">
            <div class="summary-title">✨ AI Summary</div>
            <div class="summary-content">{summary}</div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("📄 View Source Content"):
            st.markdown(f"**Source:** {original_title}")
            if url:
                st.markdown(f"[Read Original Article]({url})")
            st.divider()
            st.write(original_text)

# Footer
st.divider()
st.markdown('<p style="text-align: center; color: #94a3b8; font-size: 0.9rem;">NewsLens AI Summarizer • Powered by BART Transformer</p>', unsafe_allow_html=True)
