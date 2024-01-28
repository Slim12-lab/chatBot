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

#Возвращает отформатированный текстовый список всех пользователей в базе данных.
async def print_list(id):
     cursor.execute("SELECT id, name, secondName, phone, email FROM auth")
     data = cursor.fetchall()
     text = ''
     for row in data:
        text += f"{row[0]}. {row[1]} {row[2]} - {row[3]} - {row[4]}\n"

     return(f"\n\n{text}")

#Обновляет поле tg_id в таблице auth для указанного пользователя по его логину.
async def insert_id(user_id, login):
    cursor.execute("UPDATE auth SET tg_id = ? WHERE login = ?", (user_id, login))
    conn.commit()

#Возвращает логин заказчика (по login в таблице auth) для указанного исполнителя.
async def return_customer(perfomer_login):
    cursor.execute("SELECT login FROM auth WHERE id=?", (perfomer_login,))
    data = cursor.fetchall()
    text = ''
    for row in data:
        text += f"{row[0]}"
        return text
    conn.commit()

# Добавляет новую задачу в таблицу task.
async def insert_task(customer_login, perfomer_login, description):
    cursor.execute("INSERT INTO task (customer, performer, description) VALUES (?, ?, ?)", (customer_login, perfomer_login, description))
    conn.commit()

#Возвращает отформатированный текстовый список задач для указанного исполнителя.
async def task_list(perm):
     cursor.execute("SELECT description, customer FROM task WHERE performer=?", (perm,))
     data = cursor.fetchall()
     text = ''
     for idx, row in enumerate(data, start=1):
            text += f"{idx}. Поручение: {row[0]}\nОтправитель: {row[1]}\n\n"
     return(f"{text}")

#Возвращает отформатированный текстовый список задач для указанного заказчика.
async def task_list_myself(perm):
     cursor.execute("SELECT description, performer FROM task WHERE customer=?", (perm,))
     data = cursor.fetchall()
     text = ''
     for idx, row in enumerate(data, start=1):
            text += f"{idx}. Поручение: {row[0]}\nИспольнитель: {row[1]}\n\n"
     return(f"{text}")

#Возвращает имя и фамилию пользователя по его логину.
async def get_names(login):
    cursor.execute("SELECT name, secondName FROM auth WHERE login=?",  (login,))
    data = cursor.fetchall()
    text = ''
    for row in data:
        text += f"{row[0]} {row[1]}"
    return text
    conn.commit()

#Возвращает Telegram ID пользователя по его логину.
async def get_tgid(login):
    cursor.execute("SELECT tg_id FROM auth WHERE login=?",  (login,))
    data = cursor.fetchall()
    text = ''
    for row in data:
        text += f"{row[0]}"
        return text
    conn.commit()

# Возвращает логин пользователя по его Telegram ID.
async def return_login(id):
    cursor.execute("SELECT login FROM auth WHERE tg_id=?", (id,))
    data = cursor.fetchall()
    text = ''
    for row in data:
        text += f"{row[0]}"
        return text
    conn.commit()

#Удаляет задачу из таблицы task по номеру задачи для указанного исполнителя.
async def delete_task_by_number(perm, idx):
    try:
        idx = int(idx)  # Преобразуем idx в целое число
    except ValueError:
        return False  # Вернем False, если idx не является целым числом

    cursor.execute("SELECT id, description, customer FROM task WHERE performer=?", (perm,))
    data = cursor.fetchall()

    if 1 <= idx <= len(data):
        task_id_to_delete = data[idx - 1][0]  # Получаем id задачи по номеру idx
        cursor.execute("DELETE FROM task WHERE id=?", (task_id_to_delete,))
        conn.commit()
        return True  # Успешное удаление
    else:
        return False  # Неверный номер задачи

    conn.commit()