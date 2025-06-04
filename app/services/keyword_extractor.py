import re
from collections import Counter
from typing import List

def extract_keywords(text: str, top_n: int = 5) -> List[str]:
    russian_chars = re.findall(r'[а-яА-ЯёЁ]', text)
    is_russian = len(russian_chars) > len(text) * 0.3
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    words = text.split()
    if is_russian:
        stop_words = {'и', 'в', 'во', 'не', 'что', 'он', 'на', 'я', 'с', 'со', 'как', 'а', 'то', 'все', 'она', 'так',
                     'его', 'но', 'да', 'ты', 'к', 'у', 'же', 'вы', 'за', 'бы', 'по', 'только', 'ее', 'мне', 'было',
                     'вот', 'от', 'меня', 'еще', 'нет', 'о', 'из', 'ему'}
        min_length = 3
    else:
        stop_words = {'the', 'and', 'to', 'of', 'a', 'in', 'that', 'is', 'was', 'for', 'on', 'with', 
                     'by', 'as', 'are', 'at', 'be', 'this', 'have', 'from', 'or', 'an', 'but', 'not',
                     'they', 'which', 'you', 'one', 'all', 'would', 'there', 'their'}
        min_length = 3
    
    filtered_words = [word for word in words if word not in stop_words and len(word) > min_length]
    word_counts = Counter(filtered_words)
    keywords = [word for word, count in word_counts.most_common(top_n)] if filtered_words else []
    if len(keywords) < top_n:
        additional_words = [w for w in words if w not in stop_words and len(w) >= 2 and w not in keywords]
        additional_counts = Counter(additional_words)
        keywords.extend([w for w, c in additional_counts.most_common(top_n - len(keywords))])
    
    return keywords[:top_n]
