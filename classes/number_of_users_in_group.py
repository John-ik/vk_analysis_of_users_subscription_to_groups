from mysql.connector import connect, Error


class NumberOfUsersInGroup(object):
    """Данный класс при вызове показывает количество подписчиков выбранной группы"""

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
                count_query = f"SELECT count(id) FROM {self.group_id}"
                group_name_query = f"SELECT group_name FROM vk_ids WHERE group_id = '{self.group_id}'"
                with connection.cursor() as cursor:
                    cursor.execute(count_query)
                    number_of_users = cursor.fetchone()[0]
                    cursor.execute(group_name_query)
                    group_name = cursor.fetchone()[0]
                    print(f"Количество подписчиков {group_name}: {number_of_users}")
        except Error as e:
            print(e)
