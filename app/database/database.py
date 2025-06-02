import sqlite3

def get_db():
    connection = sqlite3.connect('database.db')
    try:
        yield connection
    finally:
        connection.close()
