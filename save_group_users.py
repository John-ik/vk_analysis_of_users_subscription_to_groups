from mysql.connector import connect, Error
import vk_api
import time


class SaveGroupUsers(object):
    """Здесь я реалезую работу с vk api через свой класс"""

    def __init__(self, group_id, token, host, user, password, database):
        self.__token = token
        self.session = vk_api.VkApi(token=self.__token)
        self.group_id = group_id
        self.db_conn_info = {"host": host, "user": user, "password": password, "database": database}
        self.check_group_table()
        print("Все участники группы сохранены.")

    def check_group_table(self):
        with connect(
                host=self.db_conn_info["host"],
                user=self.db_conn_info["user"],
                password=self.db_conn_info["password"],
                database=self.db_conn_info["database"]
        ) as connection:
            query = """
                    SHOW TABLES
                    """
            with connection.cursor() as cursor:
                cursor.execute(query)
                tables = cursor.fetchall()
            table_in_base = False
            for table in tables:
                if table[0] == self.group_id:
                    table_in_base = True
            if table_in_base:
                self.append_table(connection)
            else:
                self.create_table_for_group(connection)

    def create_table_for_group(self, connection):
        query = """
                CREATE TABLE """ + self.group_id + """(
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                group_id VARCHAR(100)
                )
                """
        with connection.cursor() as cursor:
            cursor.execute(query)
        self.get_group_members(0, connection)

    def append_table(self, connection):
        query = """
                SELECT COUNT(*) FROM """ + self.group_id + """
                """
        with connection.cursor() as cursor:
            cursor.execute(query)
            count = cursor.fetchone()[0]
        self.get_group_members(count, connection)

    def get_group_members(self, start_from, connection):
        members_count = self.session.method("groups.getMembers", {"group_id": self.group_id})["count"]
        print("Приступаем к сохранению участников группы.")
        for offset in range(start_from, members_count, 1000):
            self.members = self.session.method("groups.getMembers",
                                               {"group_id": self.group_id,
                                                "count": 1000, "offset": offset}
                                               )["items"]
            print(self.members)  # показывает список, который вноситься в данный момент
            self.save_members_to_db(connection)

    def save_members_to_db(self, connection):
        user_group_dict = []
        for user_id in self.members:
            user_group_dict.append([user_id, self.group_id])
        query = """
                INSERT INTO """ + self.group_id + """
                (user_id, group_id)
                VALUES (%s, %s)
                """
        with connection.cursor() as cursor:
            cursor.executemany(query, user_group_dict)
            connection.commit()
        time.sleep(0.3)


# if __name__ == "__main__":
#     group = Save_Group_Users("kwin_steam")
