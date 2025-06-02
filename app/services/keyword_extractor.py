from collections import Counter
from typing import List, Sequence

import yake

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk

import pymorphy2

from app.core import logging_config

logger = logging_config.setup_logger(__name__)

class TextTokenizer:
    def __init__(self):
        """
        morph - морфологический анализатор

        ACCEPTED_POS - разрешённые части речи: существительные и полные прилагательные
        """
        try:
            logger.info("Downloading data for NLTK")

            nltk.download(["punkt_tab", "stopwords"])

        except Exception as e:
            logger.error(f"Something went wrong with TextTokenizer:\n{e}")

        self.morph = pymorphy2.MorphAnalyzer()
        self.ACCEPTED_POS = {"NOUN", "ADJF"}

    def tokenize(self, text: str) -> List[str]:
        """
        Токенизирует текст, убирает стоп-слова, знаки пунктуации
        и возвращает массив токенов
        """
        logger.debug("Tokenizing text")

        tokens: List[str] = word_tokenize(text.lower())

        return self._postprocess_tokens(tokens)

    def _postprocess_tokens(self, tokens: List[str]) -> List[str]:
        """
        Обрабатывает полученные токены:
        удаляет стоп слова, знаки пунктуации,
        лемматизирует
        """

        cleaned_tokens: List[str] = self._delete_stopwords_and_punctuations(tokens)
        lemmatized_pos_tokens: List[tuple[str,str]] = self._lemmatize_with_pos(cleaned_tokens)

        lemmatized_tokens = [
            word for word, pos in lemmatized_pos_tokens if pos == "NOUN"
        ]

        bigrams = self._filter_bigrams(lemmatized_pos_tokens)

        return lemmatized_tokens + bigrams

    def _delete_stopwords_and_punctuations(self, tokens: List[str]) -> List[str]:
        """
        Удаляет стоп слова и знаки пунктуации
        """
        stop_words = set(stopwords.words("russian"))

        return [token for token in tokens 
            if token not in stop_words and 
            token.isalpha() and
            len(token) > 2
        ]

    def _generate_ngrams(self, tokens: List[str], n: int = 2) -> List[str]:
        """
        Генерирует n-граммы
        """

        return [' '.join(gram) for gram in nltk.ngrams(tokens, n)]

    def _filter_bigrams(self, tagged_tokens: List[tuple[str,str]]) -> List[str]:
        """
        Фильтрует биграммы, оставляя только сочетающиеся
        """

        bigrams: List[str] = []

        for i in range(len(tagged_tokens) - 1):
            (first_word, first_pos) = tagged_tokens[i]
            (second_word, second_pos) = tagged_tokens[i + 1]

            # Шаблон: прилагательное + существительное
            # существительное + существительное
            if (
                (first_pos == "ADJF" and second_pos == "NOUN") or 
                (first_pos == "NOUN" and second_pos == "NOUN")
            ):
                bigrams.append(f"{first_word} {second_word}")

            return bigrams

    def _lemmatize_with_pos(self, tokens: List[str]) -> List[tuple[str, str]]:
        """
        Лемматизирует токены, сохраняя часть речи
        """
        lemmatized_pos_tokens: List[tuple[str, str]] = []

        for token in tokens:
            parsed_token = self.morph.parse(token)[0]

            if parsed_token.tag.POS in self.ACCEPTED_POS:
                lemmatized_pos_tokens.append(
                    (parsed_token.normal_form, parsed_token.tag.POS)
                )
        return lemmatized_pos_tokens


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

