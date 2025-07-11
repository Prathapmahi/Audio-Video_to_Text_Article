from dotenv import load_dotenv
load_dotenv(override=True)  # → Force .env values to override existing vars

import os
# Confirm it's loaded correctly
print("🔧 GEMINI_MODEL_NAME from env:", os.getenv("GEMINI_MODEL_NAME"))

from transcription.assembly_ai import transcribe_audio
from generation.gemini_generator import generate_article
from style_check.style_enforcer import apply_style_guide
from scoring.bert_scorer import score_article
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def run_pipeline(audio_path: str):
    logging.info("🎙️ Starting article generation pipeline")

    # Step 1: Transcribe
    transcript = transcribe_audio(audio_path)
    logging.info("📝 Transcription complete.")

    # Step 2: Generate draft
    draft_article = generate_article(transcript)
    logging.info("📄 Draft article created.")

    # Step 3: Refine with grammar and style
    final_article = apply_style_guide(draft_article)
    logging.info("🧹 Article polished using grammar correction.")

    # Step 4: Score the article
    score = score_article(final_article)
    logging.info("📊 Scoring complete.")

    # Output the final result
    print("\n🧾 FINAL ARTICLE:\n")
    print(final_article)

    print("\n✅ ARTICLE SCORE:")
    for k, v in score.items():
        print(f"- {k}: {v}")

    return {
        "transcript": transcript,
        "draft": draft_article,
        "final": final_article,
        "score": score
    }

if __name__ == "__main__":
    AUDIO_PATH = r"C:\Users\Klodev\Downloads\harvard.mp3"
    result = run_pipeline(AUDIO_PATH)
