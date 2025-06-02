import re
from typing import Dict, Any

def calculate_readability(text: str) -> float:
    """
    Рассчитывает оценку читаемости текста.
    Использует упрощенную формулу индекса Флеша для русского языка.
    """
    stats = get_text_stats(text)
    
    # Формула индекса Флеша для русского языка (упрощенная)
    # 206.835 - (1.3 * средняя_длина_предложения) - (60.1 * среднее_число_слогов_на_слово)
    readability_score = 206.835 - (1.3 * stats["avg_words_per_sentence"]) - (60.1 * stats["avg_syllables_per_word"])
    
    # Ограничиваем результат от 0 до 100
    readability_score = max(0, min(100, readability_score))
    
    return round(readability_score, 1)

def interpret_readability(score: float) -> str:
    """Интерпретирует числовую оценку читаемости текста"""
    if score >= 80:
        return "Очень легкий текст (начальная школа)"
    elif score >= 70:
        return "Легкий текст (5-6 класс)"
    elif score >= 60:
        return "Достаточно легкий текст (7-8 класс)"
    elif score >= 50:
        return "Средней сложности (9-10 класс)"
    elif score >= 30:
        return "Сложный текст (высшее образование)"
    else:
        return "Очень сложный текст (научная литература)"

def get_text_stats(text: str) -> Dict[str, Any]:
    """Возвращает базовую статистику текста"""
    # Удаляем лишние пробелы
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Разбиваем текст на предложения
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # Разбиваем текст на слова
    words = re.findall(r'\w+', text.lower())
    
    # Считаем слоги (для русского языка - количество гласных)
    vowels = 'аеёиоуыэюя'
    syllables_count = sum(sum(1 for char in word if char in vowels) for word in words)
    
    # Средняя длина предложения
    avg_words_per_sentence = len(words) / max(1, len(sentences))
    
    # Среднее количество слогов на слово
    avg_syllables_per_word = syllables_count / max(1, len(words))
    
    return {
        "word_count": len(words),
        "sentence_count": len(sentences),
        "syllables_count": syllables_count,
        "avg_words_per_sentence": round(avg_words_per_sentence, 1),
        "avg_syllables_per_word": round(avg_syllables_per_word, 2)
    }

def get_detailed_metrics(text: str) -> Dict[str, Any]:
    """Возвращает подробные метрики читаемости текста"""
    stats = get_text_stats(text)
    readability_score = calculate_readability(text)
    interpretation = interpret_readability(readability_score)
    
    # Считаем уникальные слова
    words = re.findall(r'\w+', text.lower())
    unique_words_count = len(set(words))
    
    # Считаем сложные слова (содержат 4+ слога)
    vowels = 'аеёиоуыэюя'
    complex_words_count = sum(1 for word in words if sum(1 for char in word if char in vowels) >= 4)
    
    return {
        "readability_score": readability_score,
        "interpretation": interpretation,
        "basic_stats": stats,
        "additional_metrics": {
            "unique_words_count": unique_words_count,
            "unique_words_percentage": round(unique_words_count / max(1, len(words)) * 100, 1),
            "complex_words_count": complex_words_count,
            "complex_words_percentage": round(complex_words_count / max(1, len(words)) * 100, 1),
            "average_word_length": round(sum(len(word) for word in words) / max(1, len(words)), 1)
        }
    }
