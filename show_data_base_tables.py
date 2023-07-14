from mysql.connector import connect, Error


class ShowDataBaseTables(object):
    """Данный класс при вызове очищает базу данных"""

    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.show_data_base_tables()

    def show_data_base_tables(self):
        try:
            with connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database
            ) as connection:
                query = "SELECT group_name, group_id FROM vk_ids"
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    groups = cursor.fetchall()
                    print("Группы в базе ('имя', 'id'):")
                    for group in groups:
                        print(f"'{group[0]}'", '', f"'{group[1]}'")
        except Error as e:
            print(e)
