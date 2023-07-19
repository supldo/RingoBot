import sqlite3
from database import sql_queries

def database_dict(data):
    columns = [description[0] for description in data.description]
    data = data.fetchall()
    rows = {}
    for row in data:
        rows[row[0]] = {}
        for column, value in zip(columns, row):
            rows[row[0]][column] = value
    return rows


class Database:
    def __init__(self):
        self.connection = sqlite3.connect("db.sqlite3")
        self.cursor = self.connection.cursor()

    # Create Database
    def sql_create_db(self):
        if self.connection:
            print("База данных подключено!")

        self.connection.execute(sql_queries.create_user_table_query)
        self.connection.execute(sql_queries.create_answers_quiz)
        self.connection.execute(sql_queries.create_user_ban)
        self.connection.execute(sql_queries.create_user_survey)
        self.connection.execute(sql_queries.create_complaint_table)
        self.connection.commit()


    # Telegram User
    def sql_insert_user(self, id, username, first_name, last_name):
        self.cursor.execute(sql_queries.insert_user_query, (id,
                                                            username,
                                                            first_name,
                                                            last_name))
        self.connection.commit()
    def sql_select_user(self):
        self.cursor.row_factory = lambda cursor, row: {
            "row_number": row[0],
            'id': row[1],
            "username": row[2],
            "first_name": row[3],
            "last_name": row[4]}
        users = self.cursor.execute(sql_queries.select_user_query)
        return users

    def sql_select_user_query_by_username(self, user):
        self.cursor.row_factory = lambda cursor, row: {"id": row[0]}
        return self.cursor.execute(sql_queries.select_user_query_by_username, (user,))
    def sql_select_user_query_by_first_name(self, user):
        self.cursor.row_factory = lambda cursor, row: {"id": row[0]}
        return self.cursor.execute(sql_queries.select_user_query_by_first_name, (user,))
    def sql_select_user_query_by_last_name(self, user):
        self.cursor.row_factory = lambda cursor, row: {"id": row[0]}
        return self.cursor.execute(sql_queries.select_user_query_by_last_name, (user,))


    # User ban
    def sql_insert_user_ban(self, id_user, id_group, rаeason):
        self.cursor.execute(sql_queries.insert_user_ban, (id_user,
                                                          id_group,
                                                          rаeason))
        self.connection.commit()
    def sql_select_user_ban(self, id_user, id_group):
        cursor = self.cursor.execute(sql_queries.select_user_ban, (id_user, id_group))
        return database_dict(cursor)
    def select_potential_user_ban(self):
        cursor = self.cursor.execute(sql_queries.select_potential_user_ban)
        return database_dict(cursor)


    # Quiz
    def sql_insert_answers_quiz(self, id_user, quiz, quiz_option):
        self.cursor.execute(sql_queries.insert_answers_quiz, (id_user,
                                                              quiz,
                                                              quiz_option))
        self.connection.commit()

    # User survey
    def sql_insert_user_survey(self, idea, problems, assessment, user_id):
        self.cursor.execute(sql_queries.insert_user_survey, (idea,
                                                             problems,
                                                             assessment,
                                                             user_id))
        self.connection.commit()

    def sql_select_user_survey(self):
        cursor = self.cursor.execute(sql_queries.select_user_survey)
        return database_dict(cursor)

    def sql_select_user_survey_by_id(self, id):
        cursor = self.cursor.execute(sql_queries.select_user_survey_by_id, (id,))
        return database_dict(cursor)


    # Complaint
    def sql_insert_complaint_table(self, telegram_id, telegram_id_bad_user,
                                   reason, count):
        self.cursor.execute(sql_queries.insert_complaint_table, (telegram_id,
                                                                 telegram_id_bad_user,
                                                                 reason,
                                                                 count))
        self.connection.commit()

    def sql_select_complaint_table(self, user_id):
        self.cursor.row_factory = lambda cursor, row: {"count": row[0]}
        return self.cursor.execute(sql_queries.select_complaint_table, (user_id,))

    def sql_select_complaint_table_check(self, user_id, bad_user_id):
        self.cursor.row_factory = lambda cursor, row: {"count": row[0]}
        return self.cursor.execute(sql_queries.select_complaint_table_check, (user_id, bad_user_id,))
