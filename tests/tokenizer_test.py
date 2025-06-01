from src.core.tokenizer import TextTokenizer
from config import logging_config

logger = logging_config.setup_logger(__name__)

if __name__ == "__main__":
    tokenizer = TextTokenizer()
    with open("./tests/test_data/example1.txt", "r") as file:
        text: str = file.read()

    logger.debug(f"Initial text:\n{text}")

    logger.info(f"Tokens from text:\n{tokenizer.tokenize(text)}")
