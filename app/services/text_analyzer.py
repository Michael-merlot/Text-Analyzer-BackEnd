from typing import Dict, Any, List
import re
from app.services.keyword_extractor import extract_keywords
from app.services.readability_calculator import calculate_readability, get_text_stats


def analyze_text(text: str) -> Dict[str, Any]:
    
    stats = get_text_stats(text)
    keywords = extract_keywords(text)
    words = re.findall(r'\w+', text.lower())
    main_topic = "Текст"
    if keywords:
        main_topic = f"Текст о {keywords[0]}"
    
    readability_score = calculate_readability(text)
    
    analysis_result = {
        "word_count": stats["word_count"],
        "sentence_count": stats["sentence_count"],
        "readability_score": readability_score,
        "keywords": keywords,
        "main_topic": main_topic
    }
    
    return analysis_result
