from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)


def get_homepage_db_connection():
    conn = sqlite3.connect('homepage_data.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_users_table():
    conn = get_homepage_db_connection()
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        password TEXT NOT NULL,
        user_id TEXT UNIQUE NOT NULL
    );
    ''')

    conn.commit()
    conn.close()

# Bu fonksiyonu uygulama başlangıcında çağırarak tablonun oluşturulmasını sağlıyoruz
create_users_table()


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('inputName')
        password = request.form.get('inputPassword')
        user_id = request.form.get('inputID')

        if len(user_id) == 11 and user_id.isdigit():
            conn = get_homepage_db_connection()
            cur = conn.cursor()

            try:
                cur.execute('''
                    INSERT INTO users (name, password, user_id)
                    VALUES (?, ?, ?)
                ''', (name, password, user_id))

                conn.commit()
                conn.close()

                message = "Successfully logged in and data saved!"
            except sqlite3.IntegrityError:
                message = "This ID is already in use!"

            return render_template('homepage.html', message=message)
        else:
            message = "INVALID ID"
            return render_template('homepage.html', message=message)

    return render_template('homepage.html')

if __name__ == '__main__':
    app.run(debug=True)