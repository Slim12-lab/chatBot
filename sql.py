import sqlite3

# Подключение к базе данных (если файл не существует, он будет создан)
conn = sqlite3.connect('slt3.db')

# Создание курсора для выполнения SQL-запросов
cursor = conn.cursor()

# Создание таблицы "auth" с полями "id", "логин", "пароль", "почта" и "телефон"
cursor.execute('''
    CREATE TABLE IF NOT EXISTS auth (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login TEXT NOT NULL,
        password TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL, 
        name TEXT NOT NULL,
        secondName TEXT NOT NULL
    )
''')

try:
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS task (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer TEXT NOT NULL,
            performer TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT DEFAULT 'Активно' NOT NULL
        )
    ''')
    conn.commit()
    print("Таблица 'task' успешно создана.")
except sqlite3.Error as e:
    print("Ошибка при создании таблицы 'task':", e)

async def print_list(id):
     cursor.execute("SELECT id, name, secondName, phone, email FROM auth WHERE tg_id != ?", (id,))
     data = cursor.fetchall()
     text = ''
     for row in data:
        text += f"{row[0]}. {row[1]} {row[2]} - {row[3]} - {row[4]}\n"

     return(f"\n\n{text}")

async def insert_id(user_id, login):
    cursor.execute("UPDATE auth SET tg_id = ? WHERE login = ?", (user_id, login))
    conn.commit()

async def return_customer(perfomer_login):
    cursor.execute("SELECT login FROM auth WHERE id=?", (perfomer_login,))
    data = cursor.fetchall()
    text = ''
    for row in data:
        text += f"{row[0]}"
        return text
    conn.commit()

async def insert_task(customer_login, perfomer_login, description):
    cursor.execute("INSERT INTO task (customer, performer, description) VALUES (?, ?, ?)", (customer_login, perfomer_login, description))
    conn.commit()

async def task_list(perm):
     cursor.execute("SELECT description, customer FROM task WHERE performer=?", (perm,))
     data = cursor.fetchall()
     text = ''
     for idx, row in enumerate(data, start=1):
            text += f"{idx}. Поручение: {row[0]}\nОт кого: {row[1]}\n\n"
     return(f"{text}")

        
async def get_names(login):
    cursor.execute("SELECT name, secondName FROM auth WHERE login=?",  (login,))
    data = cursor.fetchall()
    text = ''
    for row in data:
        text += f"{row[0]} {row[1]}"
    return text
    conn.commit()

async def get_tgid(login):
    cursor.execute("SELECT tg_id FROM auth WHERE login=?",  (login,))
    data = cursor.fetchall()
    text = ''
    for row in data:
        text += f"{row[0]}"
        return text
    conn.commit()

async def return_login(id):
    cursor.execute("SELECT login FROM auth WHERE tg_id=?", (id,))
    data = cursor.fetchall()
    text = ''
    for row in data:
        text += f"{row[0]}"
        return text
    conn.commit()