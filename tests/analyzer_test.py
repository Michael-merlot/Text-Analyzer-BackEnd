from app.services.text_analyzer import TextAnalyzer
from app.core.logging_config import setup_logger

logger = setup_logger(__name__)
analyzer = TextAnalyzer()

epsilon = 2

def word_count_test(text: str):
    try:
        assert analyzer.get_statistic(text)["words_count"] in range(167 - epsilon, 167 + (epsilon + 1))
    except AssertionError:
        logger.error(f"Word count test failed:\n\
        Analyzer statistic:\t{analyzer.get_statistic(text)['words_count']}\n\
        Actual:\t{167}")

def char_count_test(text: str):
    try:
        assert analyzer.get_statistic(text)["chars_count"] in range(1277 - epsilon, 1277 + (epsilon + 1))
    except AssertionError:
        logger.error(f"Char count test failed:\n\
        Analyzer statistic:\t{analyzer.get_statistic(text)['chars_count']}\n\
        Actual:\t{1277}")

def sentence_count_test(text: str):
    try:
        assert analyzer.get_statistic(text)["sentences_count"] in range(11 - epsilon, 11 + (epsilon + 1))
    except AssertionError:
        logger.error(f"Sentence count test failed:\n\
        Analyzer statistic:\t{analyzer.get_statistic(text)['sentences_count']}\n\
        Actual:\t{11}")

if __name__ == "__main__":
    with open("./tests/test_data/example1.txt", "r") as file:
        text = file.read()

    word_count_test(text)
    char_count_test(text)
    sentence_count_test(text)
