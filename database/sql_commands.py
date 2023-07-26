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
        self.connection.execute(sql_queries.create_wallet)
        self.connection.execute(sql_queries.create_referral)
        self.connection.execute(sql_queries.create_anime_note)
        self.connection.commit()


    # Telegram User
    def sql_insert_user(self, id, username, first_name, last_name):
        self.cursor.execute(sql_queries.insert_user_query, (id,
                                                            username,
                                                            first_name,
                                                            last_name,
                                                            None))
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


    # Wallet
    def sql_insert_wallet(self, id):
        self.cursor.execute(sql_queries.insert_wallet, (id,))
        self.connection.commit()
    def sql_select_wallet(self, id):
        return self.cursor.execute(sql_queries.select_wallet, (id,)).fetchall()[0][0]
    def sql_update_wallet(self, id):
        self.cursor.execute(sql_queries.update_wallet, (id,))
        self.connection.commit()


    # Referral
    def sql_insert_referral(self, owner_link_telegram_id, referral_telegram_id):
        self.cursor.execute(sql_queries.insert_referral, (owner_link_telegram_id, referral_telegram_id,))
        self.connection.commit()
    def sql_select_referral(self, referral_telegram_id):
        self.cursor.row_factory = lambda cursor, row: {"id": row[0],
                                                       "owner_link_telegram_id":row[1],
                                                       "referral_telegram_id":row[2],
                                                       }
        return self.cursor.execute(sql_queries.select_referral, (referral_telegram_id,)).fetchall()
    def sql_select_all_referrals(self, user_id):
        self.cursor.row_factory = lambda cursor, row: {"id":row[0],
                                                       "username":row[1],
                                                       "first_name":row[2],
                                                       "last_name":row[3]}
        return self.cursor.execute(sql_queries.select_all_referrals, (user_id,)).fetchall()


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
    def sql_insert_complaint_table(self, telegram_id, telegram_id_bad_user, reason, count):
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


    # Reference
    def sql_update_user_reference_link(self, link, telegram_id):
        self.cursor.execute(sql_queries.update_user_reference_link_query, (link, telegram_id,))
        self.connection.commit()
    def sql_select_user_return_link(self, telegram_id):
        self.cursor.row_factory = lambda cursor, row: {"link": row[0]}
        return self.cursor.execute(
            sql_queries.select_user_by_id_return_link_query, (telegram_id,)
        ).fetchall()
    def sql_select_user_by_link(self, link):
        self.cursor.row_factory = lambda cursor, row: {"link": row[0]}
        return self.cursor.execute(sql_queries.select_user_by_link, (link,)).fetchall()


    # Anime note
    def sql_insert_anime_note(self, user_id, link_anime):
        self.cursor.execute(sql_queries.insert_anime_note, (user_id,
                                                            link_anime))
        self.connection.commit()
    def sql_select_anime_note(self, id_user):
        self.cursor.row_factory = lambda cursor, row: {"anime": row[0],
                                                       "link": row[1]}
        return self.cursor.execute(sql_queries.select_anime_note, (id_user,)).fetchall()