from mysql.connector import connect, Error
import vk_api
import time


class Vk_db_collector(object):
    """Данный класс сохраняет айди пользователей выбранной группы вконтакте в свою таблицу в базе"""

    def __init__(self, group_id):
        self.__token = """vk_account_token"""
        self.session = vk_api.VkApi(token=self.__token)
        self.group_id = group_id
        self.db_conn_info = {"host": "localhost", "user": input("Имя пользователя базы: "),
                             "password": input("Пароль пользователя базы: "),
                             "database": input("Какую использовать базу: ")}
        self.check_group_table()

    def check_group_table(self):  # проверяем, есть ли уже данная группа в базе
        try:
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
                    tables = cursor.fetchall()  # здесь группы, которые в нашей базе
                print(connection)  # показывает, что подключение к локальной базе выполнено успошно
        except Error as e:
            print(e)
        table_in_base = False
        for table in tables:
            if table[0] == self.group_id:
                table_in_base = True
        if table_in_base:  # если группа есть в базе, то дополняем её, если она не полная
            self.append_table()
        else:  # если группы нет в базе, то создаем новую таблицу группы и заполняем её
            self.create_table_for_group()

    def create_table_for_group(self):  # создаём таблицу для новой группы
        try:
            with connect(
                    host=self.db_conn_info["host"],
                    user=self.db_conn_info["user"],
                    password=self.db_conn_info["password"],
                    database=self.db_conn_info["database"]
            ) as connection:
                query = """
                        CREATE TABLE """ + self.group_id + """(
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id INT,
                        group_id VARCHAR(100)
                        )
                        """
                with connection.cursor() as cursor:
                    cursor.execute(query)
                print(connection)  # показывает, что подключение к локальной базе выполнено успошно
        except Error as e:
            print(e)
        self.get_group_members(0)

    def append_table(self):  # находим место, где мы остановились, и дополняем, начиная уже с него
        try:
            with connect(
                    host=self.db_conn_info["host"],
                    user=self.db_conn_info["user"],
                    password=self.db_conn_info["password"],
                    database=self.db_conn_info["database"]
            ) as connection:
                query = """
                        SELECT COUNT(*) FROM """ + self.group_id + """
                        """
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    count = cursor.fetchone()[0]
                print(connection)  # показывает, что подключение к локальной базе выполнено успошно
        except Error as e:
            print(e)
        self.get_group_members(count)

    def get_group_members(self, start_from):  # получаем пользователей
        members_count = self.session.method("groups.getMembers", {"group_id": self.group_id})["count"]
        for offset in range(start_from, members_count, 1000):
            self.members = self.session.method("groups.getMembers",
                                               {"group_id": self.group_id,
                                                "count": 1000, "offset": offset}
                                               )["items"]
            print(self.members)  # показывает список, который вноситься в данный момент
            self.save_members_to_db()

    def save_members_to_db(self):  # вносим пользователей в таблицу
        user_group_dict = []
        for user_id in self.members:
            user_group_dict.append([user_id, self.group_id])
        try:
            with connect(
                    host=self.db_conn_info["host"],
                    user=self.db_conn_info["user"],
                    password=self.db_conn_info["password"],
                    database=self.db_conn_info["database"]
            ) as connection:
                query = """
                        INSERT INTO """ + self.group_id + """
                        (user_id, group_id)
                        VALUES (%s, %s)
                        """
                with connection.cursor() as cursor:
                    cursor.executemany(query, user_group_dict)
                    connection.commit()
                print(connection)  # показывает, что подключение к локальной базе выполнено успошно
        except Error as e:
            print(e)
        time.sleep(0.3)


if __name__ == "__main__":
    group = Vk_db_collector("some_group_id")  # создаём объект, указывая - какую группы мы хотим внести в базу
