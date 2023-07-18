from save_group_users import SaveGroupUsers
from clear_data_base import ClearDataBase
from show_data_base_tables import ShowDataBaseTables
from number_ofUsers_in_group import NumberOfUsersInGroup
from config import vk_token, host, user, password, database

if __name__ == "__main__":
    SaveGroupUsers("id_группы", vk_token, host, user, password, database)
    ShowDataBaseTables(host, user, password, database)
