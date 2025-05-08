import sqlite3


def get_db_connection():
    conn = sqlite3.connect('homepage_data.db')
    conn.row_factory = sqlite3.Row
    return conn


def insert_user(name, password, user_id):
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute('''
            INSERT INTO users (name, password, user_id)
            VALUES (?, ?, ?)
        ''', (name, password, user_id))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return False
    conn.close()
    return True
