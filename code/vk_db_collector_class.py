from mysql.connector import connect, Error
import vk_api
import time

class Vk_db_collector(object):
    """Здесь я реалезую работу с vk api через свой класс"""

    def __init__(self, group_id):
        self.__token = "vk_account_token"
        self.session = vk_api.VkApi(token=self.__token)
        self.group_id = group_id
        self.get_group_members()

    def get_group_members(self):
        members_count = self.session.method("groups.getMembers", {"group_id": self.group_id})["count"]
        for offset in range(0, members_count, 1000):
            self.members = self.session.method("groups.getMembers",
                                          {"group_id": self.group_id,
                                           "count": 1000, "offset": offset}
                                          )["items"]
            print(self.members)
            self.save_members_to_db()

    def save_members_to_db(self):
        user_group_dict = []
        for user_id in self.members:
            user_group_dict.append([user_id, self.group_id])
        try:
            with connect(
                    host="localhost",
                    user=input("Имя пользователя: "),
                    password=input("Пароль: "),
                    database="vk_parse_db"
            ) as connection:
                query = """
                        INSERT INTO tests 
                        (user_id, group_id)
                        VALUES (%s, %s)
                        """
                with connection.cursor() as cursor:
                    cursor.executemany(query, user_group_dict)
                    connection.commit()
                print(connection)
        except Error as e:
            print(e)
        time.sleep(0.3)


if __name__ == "__main__":
    group = Vk_db_collector("some_group_id")