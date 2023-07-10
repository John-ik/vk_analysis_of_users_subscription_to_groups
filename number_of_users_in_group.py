from mysql.connector import connect, Error


class NumberOfUsersInGroup(object):
    """Данный класс при вызове очищает базу данных"""

    def __init__(self, group_id, host, user, password, database):
        self.group_id = group_id
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.number_of_users_in_group()

    def number_of_users_in_group(self):
        try:
            with connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database
            ) as connection:
                query = f"SELECT count(id) FROM {self.group_id}"
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    number_of_users = cursor.fetchone()[0]
                    print(f"Количество подписчиков {self.group_id}: {number_of_users}")
        except Error as e:
            print(e)

# if __name__ == "__main__":
#     NumberOfUsersInGroup("localhost", "ifan", "", "vk_parse_db")
