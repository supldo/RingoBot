# user
create_user_table_query = """
    CREATE TABLE IF NOT EXISTS telegram_users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username CHAR(50), 
        first_name CHAR(50),
        last_name CHAR(50)
    )
"""
insert_user_query = """INSERT OR IGNORE INTO telegram_users VALUES (?, ?, ?, ?)"""
select_user_query = """SELECT ROW_NUMBER() OVER (ORDER BY id)
                    as row_number, id, username, first_name, last_name
                    FROM telegram_users"""

select_user_query_by_username = """SELECT id FROM telegram_users WHERE username = ?"""
select_user_query_by_first_name = """SELECT id FROM telegram_users WHERE first_name = ?"""
select_user_query_by_last_name = """SELECT id FROM telegram_users WHERE last_name = ?"""


# user ban
create_user_ban = """
    CREATE TABLE IF NOT EXISTS user_ban (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_user INTEGER REFERENCES telegram_users (id),
        id_group INTEGER,
        datetime DATETIME DEFAULT (datetime('now', '+6 hours')) NOT NULL,
        rаeason TEXT
    )
"""
insert_user_ban = """INSERT INTO user_ban(id_user, id_group, rаeason) VALUES (?, ?, ?)"""
select_user_ban = """SELECT id_user FROM user_ban WHERE id_user = ? AND id_group = ? AND datetime('now', '-18 hours') < datetime('now', '+6 hours')"""

select_potential_user_ban = """
    SELECT ROW_NUMBER() OVER (ORDER BY bans.datetime DESC) AS row_number,
        users.id,
        users.username,
        users.last_name,
        users.first_name,
        bans.datetime,
        bans.rаeason
    FROM telegram_users AS users
    INNER JOIN user_ban AS bans ON bans.id_user = users.id
    WHERE datetime('now', '-18 hours') < datetime('now', '+6 hours')
    GROUP BY users.id
    ORDER BY bans.datetime DESC;
"""

# quiz
create_answers_quiz = """
    CREATE TABLE IF NOT EXISTS answers_quiz (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_user INTEGER,
        quiz CHAR(10),
        quiz_option INTEGER,
        FOREIGN KEY (id_user) REFERENCES telegram_users (id)
    )
"""
insert_answers_quiz = """INSERT INTO answers_quiz(id_user, quiz, quiz_option) VALUES (?, ?, ?)"""

# user survey
create_user_survey = """
    CREATE TABLE IF NOT EXISTS user_survey (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        idea TEXT,
        problems TEXT,
        assessment INTEGER,
        user_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES telegram_users (id)
    )
"""
insert_user_survey = """INSERT INTO user_survey(idea, problems, assessment, user_id) 
                        VALUES (?, ?, ?, ?)"""

select_user_survey = """SELECT * FROM user_survey"""

select_user_survey_by_id = """
    SELECT * FROM user_survey AS survay
    LEFT JOIN telegram_users AS user ON survay.user_id = user.id
    WHERE survay.id = ?
"""

# complaint
create_complaint_table = """
    CREATE TABLE IF NOT EXISTS complaint(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER,
        telegram_id_bad_user INTEGER,
        reason TEXT,
        count INTEGER,
        FOREIGN KEY (telegram_id) REFERENCES telegram_users (id),
        FOREIGN KEY (telegram_id_bad_user) REFERENCES telegram_users (id)
    )
"""

insert_complaint_table = """
    INSERT OR IGNORE INTO complaint(telegram_id, telegram_id_bad_user, reason, count)
    VALUES (?, ?, ?, ?)
"""

select_complaint_table = """
    SELECT count FROM complaint WHERE telegram_id_bad_user = ?
"""

select_complaint_table_check = """
    SELECT telegram_id FROM complaint WHERE telegram_id = ? AND telegram_id_bad_user = ?
"""