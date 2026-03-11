import streamlit as st
from groq import Groq

# Page configuration
st.set_page_config(
    page_title="Mindful Journal",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for classy minimalist design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Lato:wght@300;400&display=swap');

    html, body, [class*="css"] {
        font-family: 'Lato', sans-serif;
        background-color: #FAFAF8;
        color: #2C2C2C;
    }

    .main {
        background-color: #FAFAF8;
    }

    h1 {
        font-family: 'Playfair Display', serif !important;
        font-size: 2.8rem !important;
        font-weight: 400 !important;
        letter-spacing: -0.5px;
        color: #1A1A1A;
    }

    .subtitle {
        font-family: 'Lato', sans-serif;
        font-size: 0.95rem;
        color: #888;
        font-weight: 300;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 2rem;
    }

    .stTextArea textarea {
        border: 1px solid #E0DDD8 !important;
        border-radius: 4px !important;
        font-family: 'Lato', sans-serif !important;
        font-size: 1rem !important;
        font-weight: 300 !important;
        color: #2C2C2C !important;
        background-color: #FFFFFF !important;
        padding: 1.2rem !important;
        line-height: 1.8 !important;
        box-shadow: none !important;
    }

    .stTextArea textarea:focus {
        border-color: #C8A96E !important;
        box-shadow: 0 0 0 1px #C8A96E !important;
    }

    .stButton > button {
        background-color: #1A1A1A !important;
        color: #FAFAF8 !important;
        border: none !important;
        border-radius: 3px !important;
        font-family: 'Lato', sans-serif !important;
        font-size: 0.8rem !important;
        font-weight: 400 !important;
        letter-spacing: 2.5px !important;
        text-transform: uppercase !important;
        padding: 0.7rem 2.5rem !important;
        transition: background-color 0.3s ease !important;
        cursor: pointer !important;
    }

    .stButton > button:hover {
        background-color: #C8A96E !important;
    }

    .insight-card {
        background: #FFFFFF;
        border-left: 3px solid #C8A96E;
        padding: 1.8rem 2rem;
        margin-top: 2rem;
        border-radius: 0 4px 4px 0;
        box-shadow: 0 2px 12px rgba(0,0,0,0.05);
    }

    .insight-label {
        font-family: 'Lato', sans-serif;
        font-size: 0.7rem;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #C8A96E;
        margin-bottom: 0.8rem;
        font-weight: 400;
    }

    .insight-text {
        font-family: 'Playfair Display', serif;
        font-size: 1.05rem;
        line-height: 1.9;
        color: #2C2C2C;
        font-style: italic;
    }

    .mood-row {
        display: flex;
        gap: 0.8rem;
        margin-bottom: 1.5rem;
        flex-wrap: wrap;
    }

    .mood-chip {
        padding: 0.3rem 1rem;
        border: 1px solid #E0DDD8;
        border-radius: 20px;
        font-size: 0.8rem;
        color: #888;
        cursor: pointer;
        font-family: 'Lato', sans-serif;
        font-weight: 300;
        letter-spacing: 0.5px;
        transition: all 0.2s;
    }

    .divider {
        height: 1px;
        background: linear-gradient(to right, #E0DDD8, transparent);
        margin: 2rem 0;
    }

    .footer-text {
        font-size: 0.75rem;
        color: #BBBBBB;
        text-align: center;
        font-weight: 300;
        letter-spacing: 1px;
        margin-top: 3rem;
    }

    #MainMenu, footer, header {visibility: hidden;}
    .block-container {
        padding-top: 3rem !important;
        max-width: 720px !important;
    }
</style>
""", unsafe_allow_html=True)


# Initialize Groq client using Streamlit secrets
def get_client():
    return Groq(api_key=st.secrets["GROQ_API_KEY"])


# Header
st.markdown("<h1>Mindful Journal</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtitle">AI-Powered Daily Reflection</p>', unsafe_allow_html=True)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Mood selector
st.markdown("**How are you feeling right now?**")
st.markdown("""
<div class="mood-row">
  <span class="mood-chip">Calm</span>
  <span class="mood-chip">Anxious</span>
  <span class="mood-chip">Grateful</span>
  <span class="mood-chip">Overwhelmed</span>
  <span class="mood-chip">Hopeful</span>
  <span class="mood-chip">Tired</span>
  <span class="mood-chip">Energized</span>
</div>
""", unsafe_allow_html=True)

mood = st.selectbox(
    "Select your current mood",
    ["Calm", "Anxious", "Grateful", "Overwhelmed", "Hopeful", "Tired", "Energized"],
    label_visibility="collapsed"
)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Journal entry
st.markdown("**Write your thoughts...**")
journal_entry = st.text_area(
    label="Journal",
    height=200,
    placeholder="Begin with a single sentence. What happened today that stayed with you?",
    label_visibility="collapsed"
)

# Analysis type
analysis_type = st.radio(
    "What kind of reflection do you need?",
    ["Emotional Insight", "Growth Prompt", "Gratitude Reframe", "Action Plan"],
    horizontal=True,
    label_visibility="visible"
)

st.markdown("")

col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    reflect_btn = st.button("Reflect")

# Process and display insight
if reflect_btn:
    if not journal_entry.strip():
        st.warning("Please write something in your journal first.")
    else:
        # Build prompt based on analysis type
        prompts = {
            "Emotional Insight": f"""You are a compassionate journaling coach. The user feels '{mood}' today.
Analyze this journal entry and provide a brief, warm emotional insight (3-4 sentences).
Focus on identifying the core emotion, validating it, and offering a gentle reframe.
Be minimalist, thoughtful, and avoid generic advice. Write in second person.
Entry: {journal_entry}""",

            "Growth Prompt": f"""You are a life coach specializing in reflective journaling. The user feels '{mood}'.
Read this journal entry and provide 2-3 powerful introspective questions that push the user toward self-discovery.
Make the questions specific to their entry, not generic. Be concise and insightful.
Entry: {journal_entry}""",

            "Gratitude Reframe": f"""You are a mindfulness expert. The user feels '{mood}' today.
Read this journal entry and help the user find 3 specific gratitude points hidden within their experience.
Even in difficult entries, find the silver lining. Be warm but not dismissive of their struggles.
Entry: {journal_entry}""",

            "Action Plan": f"""You are a productivity coach. The user feels '{mood}' today.
Read this journal entry and create a micro action plan: 1 thing to do today, 1 thing to do this week,
and 1 mindset shift to adopt. Be specific, practical, and tied to their actual entry.
Entry: {journal_entry}"""
        }

        with st.spinner("Reflecting..."):
            try:
                client = get_client()
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are a thoughtful, minimalist journaling assistant. Be concise, warm, and deeply insightful."},
                        {"role": "user", "content": prompts[analysis_type]}
                    ],
                    max_tokens=400,
                    temperature=0.75
                )
                insight = response.choices[0].message.content

                st.markdown(f"""
                <div class="insight-card">
                    <div class="insight-label">{analysis_type}</div>
                    <div class="insight-text">{insight}</div>
                </div>
                """, unsafe_allow_html=True)

                # Show session count
                if "entry_count" not in st.session_state:
                    st.session_state.entry_count = 0
                st.session_state.entry_count += 1

                st.markdown(f'<p class="footer-text">Entry #{st.session_state.entry_count} this session &nbsp;&middot;&nbsp; Powered by Llama 3 via Groq</p>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Connection error: {str(e)}. Check your API key in secrets.")
