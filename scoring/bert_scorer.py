import os
import re
from sentence_transformers import SentenceTransformer, util
from textstat import flesch_reading_ease

# Load once
bert_model = SentenceTransformer('all-MiniLM-L6-v2')  # lightweight but effective

REFERENCE_TEMPLATE = """
Title: Understanding the Impact of AI in Business

Introduction:
Artificial Intelligence (AI) is transforming how businesses operate. From automation to predictive analytics...

Main Body:
- Use of AI in customer service (e.g., chatbots)
- Efficiency gains in logistics and operations
- Ethical concerns and transparency

Conclusion:
AI will continue to reshape industries, requiring thoughtful integration and governance.
"""

def compute_readability(text):
    return flesch_reading_ease(text)

def compute_structure_score(article):
    embeddings = bert_model.encode([article, REFERENCE_TEMPLATE], convert_to_tensor=True)
    similarity = util.cos_sim(embeddings[0], embeddings[1])
    return float(similarity[0][0])

def count_sections(text):
    headings = re.findall(r"\n[A-Z][^\n]{3,40}\n", text)
    return len(headings)

def score_article(article: str) -> dict:
    print("[INFO] Scoring article...")

    structure_score = compute_structure_score(article)
    section_count = count_sections(article)
    readability_score = compute_readability(article)

    final_score = (
        (structure_score * 0.5) +
        (min(section_count, 5) / 5 * 0.3) +
        ((readability_score or 50) / 100 * 0.2)
    )

    return {
        "structure_similarity": round(structure_score, 3),
        "section_count": section_count,
        "readability": round(readability_score or 0, 2),
        "final_score": round(final_score * 100, 2)
    }
