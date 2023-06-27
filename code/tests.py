from mysql.connector import connect, Error
import vk_api
import time

token = "vk_account_token"
session = vk_api.VkApi(token=token)
vk = session.get_api()

def get_group_members(group_id):
    members_count = session.method("groups.getMembers", {"group_id": group_id})["count"]
    for offset in range(0, members_count, 1000):
        members = session.method("groups.getMembers", {"group_id": group_id, "count": 1000, "offset": offset})["items"]
        print(members)
        user_group_dict = []
        for user_id in members:
            user_group_dict.append([user_id, group_id])
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

get_group_members("rddm_official")
