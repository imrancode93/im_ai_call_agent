import streamlit as st
import os
from dotenv import load_dotenv
from transcriber import transcribe_audio
from agent import SalesCallAgent
import tempfile

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="AI Sales Call Assistant",
    page_icon="🎙️",
    layout="centered"
)

# Minimal, modern CSS
st.markdown(
    """
    <style>
    body {
        background-color: #f5f7fa;
    }
    .main-content {
        max-width: 700px;
        margin: 2rem auto;
        padding: 2.5rem 2rem 2rem 2rem;
        background: #fff;
        border-radius: 16px;
        box-shadow: 0 4px 24px rgba(44,62,80,0.08);
    }
    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin-top: 2rem;
        margin-bottom: 0.5rem;
        color: #2c3e50;
    }
    .summary-box, .action-box {
        background: #f8fafc;
        border-radius: 10px;
        box-shadow: 0 1px 4px rgba(44,62,80,0.04);
        padding: 1.1rem 1.3rem;
        margin-bottom: 1.2rem;
    }
    .action-list li {
        margin-bottom: 0.5rem;
        font-size: 1.08rem;
    }
    .stTextArea textarea {
        background-color: #f4f6fb;
        font-size: 1.1rem;
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar for instructions/branding
with st.sidebar:
    st.image("https://img.icons8.com/ios-filled/100/000000/phone-office.png", width=60)
    st.markdown("""
    ## Welcome!
    This assistant helps you:
    - Transcribe sales calls
    - Get executive summaries
    - Extract action items
    
    **Upload an MP3 file to get started!**
    """)

# Initialize session state
if 'transcription' not in st.session_state:
    st.session_state.transcription = None
if 'summary' not in st.session_state:
    st.session_state.summary = None
if 'action_items' not in st.session_state:
    st.session_state.action_items = None
if 'calendar' not in st.session_state:
    st.session_state.calendar = None
if 'web_search' not in st.session_state:
    st.session_state.web_search = None

def main():
    # Only render the main content container if there is content or always for the main UI
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    st.markdown("""
    <div style='display: flex; align-items: center; gap: 1rem; justify-content: center;'>
        <span style='font-size:2.2rem;'>🎙️</span>
        <span style='font-size:2rem; font-weight: 800; letter-spacing: -1px;'>AI Sales Call Assistant</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div style='margin-top: 0.5rem; margin-bottom: 2rem; font-size:1.1rem; text-align:center;'>
        Upload your sales call recording (<b>MP3 format</b>) to get a full transcription, executive summary, and action items.
    </div>
    """, unsafe_allow_html=True)

    # File uploader with clear label
    uploaded_file = st.file_uploader("Upload an MP3 file", type=['mp3'])

    if uploaded_file is not None:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name

        try:
            with st.spinner('Transcribing audio...'):
                # Transcribe audio
                transcription = transcribe_audio(tmp_file_path)
                st.session_state.transcription = transcription

            # Initialize agent and process transcription
            with st.spinner('Analyzing call content...'):
                agent = SalesCallAgent()
                agent_output = agent.process_transcription(transcription)
                st.session_state.summary = agent_output.get('summary', '')
                st.session_state.action_items = agent_output.get('action_items', [])
                st.session_state.calendar = agent_output.get('calendar', '')
                st.session_state.web_search = agent_output.get('web_search', '')

            # Clean up temporary file
            os.unlink(tmp_file_path)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            return

    # Divider for results (only if there is any result)
    if (
        st.session_state.transcription or st.session_state.summary or st.session_state.action_items or
        st.session_state.calendar or st.session_state.web_search
    ):
        st.markdown("<hr style='margin:2rem 0 1.5rem 0; border:1px solid #e1e4e8;' />", unsafe_allow_html=True)

    # Only render Transcription section if there is content
    if st.session_state.transcription:
        st.markdown('<div class="section-title">📝 Transcription</div>', unsafe_allow_html=True)
        st.markdown('<div class="summary-box">', unsafe_allow_html=True)
        st.text_area("Full transcription", st.session_state.transcription, height=180)
        st.markdown('</div>', unsafe_allow_html=True)

    # Only render Executive Summary section if there is content
    if st.session_state.summary:
        st.markdown('<div class="section-title">📊 Executive Summary</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="summary-box">{st.session_state.summary}</div>', unsafe_allow_html=True)

    # Only render Action Items section if there is content
    if st.session_state.action_items:
        st.markdown('<div class="section-title">✅ Action Items</div>', unsafe_allow_html=True)
        st.markdown('<div class="action-box">', unsafe_allow_html=True)
        action_items = st.session_state.action_items
        # If action_items is a single string, split by numbering or newlines
        if isinstance(action_items, str):
            import re
            # Split by numbered list or newlines
            items = re.split(r'\d+\.\s+', action_items)
            items = [item.strip() for item in items if item.strip()]
        else:
            items = action_items
        for item in items:
            st.checkbox(item, value=False, key=f"action_{item[:20]}")
        st.markdown('</div>', unsafe_allow_html=True)

    # Only render Calendar section if there is content
    if st.session_state.calendar:
        st.markdown('<div class="section-title">📅 Calendar</div>', unsafe_allow_html=True)
        cal_result = st.session_state.calendar
        if "Event created:" in cal_result and "http" in cal_result:
            # Extract the link
            import re
            match = re.search(r"(https?://[\w./?=&%-]+)", cal_result)
            if match:
                link = match.group(1)
                st.success(f"Meeting scheduled! [View in Google Calendar]({link})")
            else:
                st.success(cal_result)
        elif "Failed to create event" in cal_result:
            st.error(cal_result)
        else:
            st.info(cal_result)

    # Only render Web Search section if there is content
    if st.session_state.web_search:
        st.markdown('<div class="section-title">🌐 Web Search</div>', unsafe_allow_html=True)
        ws_result = st.session_state.web_search
        import re
        # Try to extract URLs and titles if present
        urls = re.findall(r"(https?://[\w./?=&%-]+)", ws_result)
        if urls:
            st.markdown('<div class="summary-box"><b>Top Results:</b><ul>', unsafe_allow_html=True)
            for url in urls:
                st.markdown(f'<li><a href="{url}" target="_blank">{url}</a></li>', unsafe_allow_html=True)
            st.markdown('</ul></div>', unsafe_allow_html=True)
        else:
            # Try to extract a web search section from the agent output
            match = re.search(r'Web Search:(.*?)(?:\n\n|$)', ws_result, re.DOTALL)
            if match:
                st.markdown(f'<div class="summary-box">{match.group(1).strip()}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="summary-box">{ws_result}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main() 