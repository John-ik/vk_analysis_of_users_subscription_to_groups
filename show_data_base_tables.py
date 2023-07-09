from mysql.connector import connect, Error


class ShowDataBaseTables(object):
    """Данный класс при вызове очищает базу данных"""

    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.clear_data_base()

    def clear_data_base(self):
        try:
            with connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database
            ) as connection:
                query = "SHOW TABLES"
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    tables = cursor.fetchall()
                    print("Таблицы в базе:")
                for table in tables:
                    print(table[0])
        except Error as e:
            print(e)

# if __name__ == "__main__":
#     Show_Data_Base_Tables("localhost", "ifan", "", "vk_parse_db")
