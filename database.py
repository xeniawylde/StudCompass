import sqlite3


#ф-ия создания таблиц
def tabl_db():
    con = sqlite3.connect('database.db')
    cursor = con.cursor()

    #таблица прдметов
    #создаем таблицу
    #задаём тип данных айди и уникальность по ключу генерир само
    #тип данных и избегаем пустого поля
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subjects(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
)
""")


    #таблица вопросов
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_id INTEGER,
        text TEXT NOT NULL,
        status TEXT DEFAULT "Не знаю", 
        answer_text TEXT,
        FOREIGN KEY (subject_id) REFERENCES subjects(id)
)
""")
    #status TEXT DEFAULT определили статус в таблице и последн строка ограничитель на сущ
    con.commit()
    con.close()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_id INTEGER,
        text TEXT NOT NULL,
        answer_text TEXT,  # 
        status TEXT DEFAULT 'Не знаю', 
        FOREIGN KEY (subject_id) REFERENCES subjects(id)
)
""")


#добавляем новую папку с предметом пользователь создает ее сам
def add_question(subject_id, question_text,  answer_text):
    con = sqlite3.connect('database.db', isolation_level=None)
    cursor = con.cursor()
    # Теперь передаем 3 значения
    cursor.execute(
        'INSERT INTO questions (subject_id, text, status, answer_text) VALUES (?, ?, ?, ?)', 
        (subject_id, question_text,'Не знаю', answer_text)
    )
    con.commit()
    con.close()



def add_subject(name):
    con = sqlite3.connect('database.db')
    cursor = con.cursor()
    cursor.execute('INSERT INTO subjects (name) VALUES (?)', (name,))
    con.commit()
    con.close()


#получаем все предметы
def get_all_subjects():
    con = sqlite3.connect('database.db')
    cursor = con.cursor()
    # Берем все предметы
    cursor.execute('SELECT * FROM subjects')
    rows = cursor.fetchall()
    con.close()
    return rows #список 



# #ф-ия добавления вопроса с привязкой к предмету
# def add_question(subject_id, question_text):
#     con = sqlite3.connect('database.db', isolation_level=None)
#     cursor = con.cursor()
#     # Явно указываем колонки! subject_id в subject_id, text в text.
#     cursor.execute(
#         'INSERT INTO questions (subject_id, text) VALUES (?, ?)', 
#         (subject_id, question_text)
#     )
#     con.commit()
#     con.close()

#создаем новую ф-ию которая достаёт из базы вопросы и фильтрует по папке

def get_all_questions_by_subject(subject_id):
    con = sqlite3.connect('database.db', isolation_level=None)#отключает кэширование транзакций данные всегда будут свежими
    cursor = con.cursor()

    cursor.execute('SELECT * FROM questions WHERE subject_id = ?', (subject_id,)) #принимает айди предмета и показывает вопросы выбранной папки
    rows = cursor.fetchall()# этой командой забираем данные

    con.close()
    return rows


def update_status(question_id, new_status):
    con = sqlite3.connect('database.db')
    cursor = con.cursor()
    #обновить табл вопросов установи статус равный айди
    cursor.execute(
        'UPDATE questions SET status = ? WHERE id=?',
        (new_status, question_id)
    )
    con.commit()
    con.close()


# def delete_empty_subjects():
#     con = sqlite3.connect('database.db')
#     cursor = con.cursor()
#     # Удаляем те предметы, где имя пустое или состоит из пробелов
#     cursor.execute("DELETE FROM subjects WHERE name IS NULL OR TRIM(name) = ''")
#     con.commit()
#     con.close()
#     print("Пустые папки удалены!")


# def fix_questions_table():
#     con = sqlite3.connect('database.db')
#     cursor = con.cursor()
#     try:
#         # Пытаемся добавить колонку subject_id
#         cursor.execute("ALTER TABLE questions ADD COLUMN subject_id INTEGER")
#         print("Колонка subject_id успешно добавлена!")
#     except sqlite3.OperationalError:
#         # Если колонка уже есть, ничего не делаем
#         print("Колонка subject_id уже существует.")
#     con.commit()
#     con.close()


def get_random_question(subject_id):
    con = sqlite3.connect('database.db', isolation_level=None)
    cursor = con.cursor()
    # ORDER BY RANDOM() выбирает случайную строку, LIMIT 1 берет только одну
    cursor.execute('SELECT * FROM questions WHERE subject_id = ? ORDER BY RANDOM() LIMIT 1', (subject_id,))
    row = cursor.fetchone()
    con.close()
    return row

def delete_question(question_id):
    con = sqlite3.connect('database.db', isolation_level=None)
    cursor = con.cursor()
    cursor.execute('DELETE FROM questions WHERE id = ?', (question_id,))
    con.commit()
    con.close()

def delete_subject(subject_id):
    con = sqlite3.connect('database.db', isolation_level=None)
    cursor = con.cursor()
    
    # 1. Сначала удаляем все вопросы, привязанные к этой папке
    cursor.execute('DELETE FROM questions WHERE subject_id = ?', (subject_id,))
    
    # 2. Потом удаляем саму папку
    cursor.execute('DELETE FROM subjects WHERE id = ?', (subject_id,))
    
    con.commit()
    con.close()



def add_questions_from_list(subject_id, questions_list):
    con = sqlite3.connect('database.db', isolation_level=None)
    cursor = con.cursor()
    
    # Проходимся по каждому вопросу в списке и вставляем его
    for q_text in questions_list:
        # Очищаем от лишних пробелов
        clean_text = q_text.strip()
        if clean_text: # Если строка не пустая
            cursor.execute(
                'INSERT INTO questions (subject_id, text, status, answer_text) VALUES (?, ?, ?, ?)',
                (subject_id, clean_text, 'Не знаю', '')
            )
    con.commit()
    con.close()

def update_answer(question_id, new_answer):
    con = sqlite3.connect('database.db', isolation_level=None)
    cursor = con.cursor()
    cursor.execute(
        'UPDATE questions SET answer_text = ? WHERE id = ?',
        (new_answer, question_id)
    )
    con.commit()
    con.close()


#запуск создания БД
if __name__ =='__main__':
    tabl_db()
    print("База данных успешно создана/обновлена!")
    input("\nНажми Enter, чтобы закрыть окно...")
#__name__ =='__main__' работает как "защита" от автомат запуска
#это всё позволяет выполнить определённый блок кода только в случае прямого запуска скрипта



