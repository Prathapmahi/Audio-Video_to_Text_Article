from happytransformer import HappyTextToText

# Load the grammar corrector model
happy_tt = HappyTextToText("T5", "prithivida/grammar_error_correcter_v1")

def apply_style_guide(text: str) -> str:
    print("[INFO] Applying grammar correction using Happy Transformer...")
    return happy_tt.generate_text(f"gec: {text}").text
