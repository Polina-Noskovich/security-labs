import sqlite3

DB_PATH = "secure_db.sqlite"

def unsafe_get_user(username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    query = f"SELECT * FROM users WHERE username = '{username}'"
    print("Выполняемый запрос:", query) 
    cursor.execute(query)
    
    user = cursor.fetchall()
    conn.close()
    
    if user:
        print("Найденные пользователи:", user)
    else:
        print("Пользователь не найден")

if __name__ == "__main__":
    unsafe_get_user("' OR '1'='1") 
