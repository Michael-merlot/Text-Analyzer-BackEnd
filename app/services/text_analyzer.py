from typing import List
import app.services.keyword_extractor as keyword_extractor
from app.core.logging_config import setup_logger

logger = setup_logger(__name__)

class TextAnalyzer:
    def __init__(self):
        self.extractor = keyword_extractor.KeywordExtractor()
        self.tokenizer = keyword_extractor.TextTokenizer()

    def get_statistic(self, text: str, n_keywords: int = 10) -> dict:
        """
        Выдаёт статистику по тексту в виде словаря:
        1. Ключевые слова
        2. Количество слов в тексте
        3. Количество предложений в тексте
        4. Количество символов в тексте

        text - текст для анализа
        n_keywords - количество ключевых слов, которые нужно вывести
        """

        logger.info("Getting statistic")

        top_n_keywords: List[str] = self.extractor.extract_keywords_tf(text, n_keywords) 
        words: List[str]          = self.tokenizer.tokenize_by_words(text)
        sentences: List[str]      = self.tokenizer.tokenize_by_sentences(text)
        chars_count: int          = len(text)

        logger.debug(f"Tokenized by words:\n{self.tokenizer.tokenize_by_words(text)}")

        return {
            "top_keywords":    top_n_keywords,
            "words_count":     len(words),
            "sentences_count": len(sentences),
            "chars_count":     chars_count
        }
