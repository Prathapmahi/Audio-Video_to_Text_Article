import streamlit as st
import tempfile
import os
from transcription.assembly_ai import transcribe_audio
from generation.gemini_generator import generate_article
from style_check.style_enforcer import apply_style_guide
from scoring.bert_scorer import score_article

st.set_page_config(page_title="AI Article Writer", layout="wide")

def load_css():
    css = """
    <style>
    .stApp {
        background: linear-gradient(315deg, #4f2991 0%, #7dc4ff 35%, #36cfcc 65%, #a92ed3 100%);
        background-size: 400% 400%;
        animation: gradientBG 20s ease infinite;
    }
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .fade-in {
        animation: fadeIn 0.8s ease-in-out both;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    button.stButton>button {
        background-color: #6200ea;
        color: white;
        padding: 0.6em 1.2em;
        border-radius: 0.4em;
        font-size: 1rem;
        transition: background-color 0.3s ease, transform 0.2s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    button.stButton>button:hover {
        background-color: #3700b3;
        transform: translateY(-2px);
    }

    /* 🌀 Better Spinner */
    .stSpinner {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    .stSpinner>div {
        border: 4px solid rgba(0,0,0,0.1);
        border-top: 4px solid #ffffff;
        border-radius: 50%;
        width: 2.2rem;
        height: 2.2rem;
        animation: spin 1s linear infinite;
    }
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    /* Make spinner text more visible */
    .stSpinner + div {
        color: white !important;
        font-size: 1rem;
        font-weight: 600;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Load CSS globally
load_css()

st.title("🎙️ AI-Powered Article Generator", anchor=None, )

audio_uploader = st.file_uploader(
    "Upload audio/video file", type=["mp3", "wav", "mp4", "m4a"]
)

if audio_uploader:
    st.audio(audio_uploader.read(), format=audio_uploader.type)

    if st.button("Run Pipeline"):
        st.write("", unsafe_allow_html=True)  # Trigger button style
        with st.spinner("✅ Transcribing..."):
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(audio_uploader.name)[1])
            tmp.write(audio_uploader.getvalue())
            tmp.flush()
            transcript = transcribe_audio(tmp.name)
            tmp.close()
        st.success("Transcription complete")

        with st.spinner("📝 Generating draft..."):
            draft = generate_article(transcript)
        st.subheader("Draft Article", anchor=None)
        st.markdown(f'<div class="fade-in">{draft}</div>', unsafe_allow_html=True)

        with st.spinner("🧹 Applying grammar/style corrections..."):
            final = apply_style_guide(draft)
        st.subheader("Final Article", anchor=None)
        st.markdown(f'<div class="fade-in">{final}</div>', unsafe_allow_html=True)

        with st.spinner("📊 Scoring article..."):
            score = score_article(final)
        st.subheader("Article Score", anchor=None)
        st.markdown('<div class="fade-in">', unsafe_allow_html=True)
        for k, v in score.items():
            st.write(f"- **{k}**: {v:.2f}")
        st.markdown('</div>', unsafe_allow_html=True)

        st.download_button(
            "📥 Download Final Article",
            final,
            file_name="article.txt",
            mime="text/plain"
        )

        os.unlink(tmp.name)
