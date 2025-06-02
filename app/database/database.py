import sqlite3


def get_db():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    try:
        yield connection
    finally:
        connection.close()