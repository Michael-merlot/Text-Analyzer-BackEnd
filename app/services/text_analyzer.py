from typing import Dict, Any
from app.services.keyword_extractor import extract_keywords
from app.services.readability_calculator import calculate_readability, get_text_stats
import re

def analyze_text(text: str) -> Dict[str, Any]:
    stats = get_text_stats(text)
    keywords = extract_keywords(text)
    main_topic = "Текст"
    if keywords:
        main_topic = f"Текст о {keywords[0]}"

    readability_score = calculate_readability(text)
    
    result = {
        "word_count": stats["word_count"],
        "sentence_count": stats["sentence_count"],
        "readability_score": readability_score,
        "keywords": keywords,
        "main_topic": main_topic
    }
    
    return result
