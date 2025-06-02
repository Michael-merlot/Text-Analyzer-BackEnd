def create_document(db, document):
    cursor = db.cursor()
    cursor.execute(
        """
        INSERT INTO documents 
        (title, content, word_count, sentence_count, readability_score, keywords)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (document.title,
         document.content,
         document.word_count,
         document.sentence_count,
         document.readability_score,
         document.keywords)

    )
    db.commit()

def get_document():
    pass