from src.core.keyword_extractor import KeywordExtractor
from config import logging_config

logger = logging_config.setup_logger(__name__)

if __name__ == "__main__":
    extractor = KeywordExtractor()
    with open("./tests/test_data/example1.txt", "r") as file:
        text: str = file.read()

    n = int(input("Top N words:\n>>>"))
    kw_tf   = extractor.extract_keywords_tf(text, top_n=n)
    kw_yake = extractor.extract_keywords_yake(text, top_n=n)

    logger.info("Keywords with TF:")

    for i in range(n):
        logger.info(f"{i}. {kw_tf[i]}")

    print("\n")

    logger.info("Keywords with YAKE:")

    for i in range(n):
        logger.info(f"{i}. {kw_yake[i]}")
