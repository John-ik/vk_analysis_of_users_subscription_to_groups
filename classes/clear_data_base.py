from mysql.connector import connect, Error


class ClearDataBase(object):
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
                for table in tables:
                    query = f"DROP TABLE {table[0]}"
                    with connection.cursor() as cursor:
                        cursor.execute(query)
                print("Таблицы успешно удалены.")
        except Error as e:
            print(e)

# if __name__ == "__main__":
#     Clear_Data_Base("localhost", "ifan", "", "vk_parse_db")
