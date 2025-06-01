from collections import Counter
from typing import List, Sequence
from src.core.tokenizer import TextTokenizer

import yake

class KeywordExtractor:
    def __init__(self):
        self.tokenizer = TextTokenizer()
        self.yake_extractor = yake.KeywordExtractor(lan="ru")

    def extract_keywords_tf(self, text: str, top_n: int = 5) -> List[str]:
        """
        Вытаскивает ключевые слова из текста с помощью
        алгоритма TF - частотный анализ
        """

        tokens: List[str] = self.tokenizer.tokenize(text)
        
        counter = Counter(tokens)

        return [token for token, _ in counter.most_common(top_n)]

    def extract_keywords_yake(self, text: str, top_n: int = 5) -> Sequence[str]:
        """
        Вытаскивает ключевые слова из текста с помощью
        библиотеки yake
        """

        self.yake_extractor.top = top_n
        kw_tuples = self.yake_extractor.extract_keywords(text)

        keywords = [word for word, _ in kw_tuples]

        return keywords

