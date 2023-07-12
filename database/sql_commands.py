import sqlite3
from database import sql_queries


class Database:
    def __init__(self):
        self.connection = sqlite3.connect("db.sqlite3")
        self.cursor = self.connection.cursor()

    def sql_create_db(self):
        if self.connection:
            print("Database connected successfully")

        self.connection.execute(sql_queries.create_user_table_query)
        self.connection.execute(sql_queries.create_answers_quiz)
        self.connection.execute(sql_queries.create_user_ban)
        self.connection.commit()

    def sql_insert_user(self, id, username, first_name, last_name):
        self.cursor.execute(sql_queries.insert_user_query, (id,
                                                            username,
                                                            first_name,
                                                            last_name))
        self.connection.commit()

    def sql_insert_user_ban(self, id_user, id_group, rаeason):
        self.cursor.execute(sql_queries.insert_user_ban, (id_user,
                                                          id_group,
                                                          rаeason))
        self.connection.commit()

    def sql_insert_answers_quiz(self, id_user, quiz, quiz_option):
        self.cursor.execute(sql_queries.insert_answers_quiz, (id_user,
                                                              quiz,
                                                              quiz_option))
        self.connection.commit()

    def sql_select_user(self):
        return self.cursor.execute(sql_queries.select_user_query).fetchall()

    def sql_select_user_ban(self, id_user, id_group):
        return self.cursor.execute(sql_queries.select_user_ban, (id_user, id_group)).fetchall()

    def select_potential_user_ban(self):
        return self.cursor.execute(sql_queries.select_potential_user_ban).fetchall()