import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables at module load
load_dotenv()

# Retrieve API key and model name (fallback to 2.5 Flash)
api_key = os.getenv("GEMINI_API_KEY")
model_name = os.getenv("GEMINI_MODEL_NAME", "models/gemini-2.5-flash").strip()

if not api_key:
    raise ValueError("❌ GEMINI_API_KEY not set in .env")

# Configure Gemini with the correct API key
genai.configure(api_key=api_key)

# Debug statement to confirm the model being used
print("[DEBUG] Using Gemini model:", model_name)

# Load the specified Gemini model
try:
    model = genai.GenerativeModel(model_name=model_name)
except Exception as e:
    raise RuntimeError(f"❌ Failed to load Gemini model '{model_name}': {e}")

# Define the article generation prompt
ARTICLE_PROMPT_TEMPLATE = """
SYSTEM:
You are a professional AI writer producing polished articles aligned with our style guide.

TASK:
- Read the following style guide.
- Write an article with: Title, Intro, subheadings, clear structure, bullet points where appropriate, formal tone, no personal opinions or vague phrases, correct grammar.

STYLE GUIDE:
{style_guide}  # e.g., include voice, grammar rules, avoid jargon, sentence length, vocabulary

TRANSCRIPT:
\"\"\"
{transcript}
\"\"\"

OUTPUT FORMAT:
1. Title (<=10 words)
2. Intro (50–100 words)
3. Sections with headings and body text
4. Conclusion (<=100 words)

Do not label sections “Section 1” etc. Start right with content.

"""

def generate_article(transcript: str, style_guide: str = "formal_business") -> str:
    """
    Generate an article from the transcript using Gemini API
    """
    print("[INFO] Generating article using Gemini...")

    if not transcript or not transcript.strip():
        raise ValueError("❌ Transcript is empty. Cannot generate article.")

    prompt = ARTICLE_PROMPT_TEMPLATE.format(
        transcript=transcript.strip(),
        style_guide=style_guide
    )

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        raise RuntimeError(f"Error in Gemini API: {e}")
