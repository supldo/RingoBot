create_user_table_query = """
        CREATE TABLE IF NOT EXISTS telegram_users
        (id CHAR(10) PRIMARY KEY, username CHAR(50), 
        first_name CHAR(50), last_name CHAR(50))
"""

insert_user_query = """INSERT INTO telegram_users VALUES (?, ?, ?, ?)"""

create_answers_quiz = """
        CREATE TABLE IF NOT EXISTS answers_quiz
        (id INTEGER PRIMARY KEY AUTOINCREMENT, id_user CHAR(10),
        quiz CHAR(10), quiz_option INTEGER,
        FOREIGN KEY (id_user) REFERENCES telegram_users (id))
"""

insert_answers_quiz = """INSERT INTO answers_quiz(id_user, quiz, quiz_option) VALUES (?, ?, ?)"""
