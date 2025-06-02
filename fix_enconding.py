import os
import codecs

def fix_file_encoding(file_path):
    try:
        # Попытка чтения файла в различных кодировках
        content = None
        encodings = ['cp1251', 'latin-1', 'utf-8-sig']
        
        for enc in encodings:
            try:
                with codecs.open(file_path, 'r', encoding=enc) as f:
                    content = f.read()
                break
            except UnicodeDecodeError:
                continue
        
        if content:
            # Сохранение с правильной кодировкой UTF-8
            with codecs.open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed encoding for {file_path}")
        else:
            print(f"Could not detect encoding for {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                fix_file_encoding(os.path.join(root, file))

# Запуск скрипта
if __name__ == "__main__":
    project_dir = os.path.dirname(os.path.abspath(__file__))
    process_directory(project_dir)
