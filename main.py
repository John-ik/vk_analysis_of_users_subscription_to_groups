from classes_main import *
from config import vk_token, host, user, password, database

if __name__ == "__main__":
    SaveGroupUsers("id_group", vk_token, host, user, password, database)
    ShowDataBaseTables(host, user, password, database)
