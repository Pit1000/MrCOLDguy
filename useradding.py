import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash

DATABASE = 'C:/Users/Manty/OneDrive/Dokumenty/flask_app/temp.db'

try:
    username = "piter"
    password = "12"
    hash = generate_password_hash(password, method='pbkdf2', salt_length=16)
    with sqlite3.connect(DATABASE) as con:
        cur = con.cursor()
        cur.execute('''INSERT INTO users (username, hash) VALUES(?, ?)''',
                    ((username, hash)))
        con.commit()
        msg = "Record successfully added"
except:
    con.rollback()
    msg = "error in insert operation"

finally:
    con.close()
