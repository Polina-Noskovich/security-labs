import sqlite3

DB_PATH = "secure_db.sqlite" 

def clear_users():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users") 
    conn.commit()
    conn.close()
    print("Все пользователи удалены!")

def safe_insert_user(username, password):
    conn = sqlite3.connect(DB_PATH) 
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        print("Пользователь добавлен успешно!")
    except sqlite3.IntegrityError:
        print("Ошибка: имя пользователя уже существует!")
    finally:
        conn.close()  

def safe_get_user(username):
    conn = sqlite3.connect(DB_PATH) 
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()  
    if user:
        print("Найден пользователь:", user)
    else:
        print("Пользователь не найден")

def initialize_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()  

if __name__ == "__main__":
    clear_users() 
    initialize_db()

    safe_insert_user("admin", "securepassword")
    safe_get_user("admin")  

    safe_get_user("' OR '1'='1")  
    
    safe_insert_user("user1", "mypassword")
    safe_get_user("user1")  