import flet as ft
from local_vk_parse_project.config import host, user, password, database, vk_token
from local_vk_parse_project.classes_main import *

def groups_ft_table():
    sql_column = ShowDataBaseTables(host, user, password, database).groups
    lines = []
    for line in sql_column:
        data_row = ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(line[0])),
                ft.DataCell(ft.Text(
                    color=ft.colors.BLUE,
                    spans=[ft.TextSpan(
                        text=line[1][0:-1],
                        url=f"https://vk.com/{line[1]}"
                    )]))
            ]
        )
        lines.append(data_row)

    ft_table = ft.DataTable(
        width=1700,
        columns=[
            ft.DataColumn(ft.Text("Имя группы")),
            ft.DataColumn(ft.Text("ID группы"))
        ],
        rows=lines)
    column = ft.Column(controls=[ft_table], scroll=ft.ScrollMode.ALWAYS, height=900)
    return column


def search_intersections_screen():
    def make_ft_data_table(users, searching_groups_count):
        intersections_count = 0
        lines = []
        for user in users:
            intersections_count += 1
            data_row = ft.DataRow(
                cells=[
                    ft.DataCell(
                        ft.Text(color=ft.colors.BLUE,
                                spans=[ft.TextSpan(
                                    text=user[0],
                                    url=f"https://vk.com/id{int(user[0])}"
                                )]),
                    ),
                    ft.DataCell(ft.Text(user[1])),
                    ft.DataCell(ft.Text(user[2])),
                    ft.DataCell(ft.Text(user[3]))
                ]
            )
            lines.append(data_row)
        ft_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Имя Фамилия")),
                ft.DataColumn(ft.Text("Дата рождения")),
                ft.DataColumn(ft.Text("Место обучения"))
            ],
            rows=lines
        )

        list_information = [ft.Text(f"Количество групп: {groups_count}", size=20),
                            ft.Text(f"Количество выбранных групп: {searching_groups_count}", size=20),
                            ft.Text(f"Koличество пересечений: {intersections_count}", size=20),
                            ft_table
                            ]
        information_column = ft.Column(spacing=10, controls=list_information,
                                       scroll=ft.ScrollMode.ALWAYS,
                                       height=900)
        page_row.controls[1] = information_column

    def start_search_intersections(e):
        print("Поиск начат")
        searching_groups = []
        for line_i in range(len(column_list)):
            group_id = ""
            if 0 < line_i < groups_count + 1:
                if column_list[line_i].value == True:
                    group_id = column_list[line_i].label.split('"')[3]
            if group_id != "":
                searching_groups.append(group_id)

        print(searching_groups)
        searching_groups_count = len(searching_groups)

        if searching_groups:
            users = SearchForIntersections(searching_groups, host, user, password, database).users
            print(users)
            make_ft_data_table(users, searching_groups_count)
            page_row.update()

    print("экран выбора групп для поиска пересечений")
    sql_column = ShowDataBaseTables(host, user, password, database).groups
    column_list = [ft.Text("Выбор группы для поиска пересечений")]
    groups_count = 0
    for line in sql_column:
        column_list.append(ft.Checkbox(label=f'"{line[0]}" "{line[1]}"', value=False))
        groups_count += 1

    users_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Имя Фамилия")),
            ft.DataColumn(ft.Text("Дата рождения")),
            ft.DataColumn(ft.Text("Место обучения"))
        ]
    )
    searching_group_count = 0
    intersections_count = 0
    list_information = [ft.Text(f"Количество групп: {groups_count}", size=20),
                        ft.Text(f"Количество выбранных групп: {searching_group_count}", size=20),
                        ft.Text(f"Koличество пересечений: {intersections_count}", size=20),
                        users_table
                        ]
    information_column = ft.Column(spacing=10, controls=list_information, scroll=ft.ScrollMode.ALWAYS,
                                   height=900)

    submit_button = ft.ElevatedButton(text="Поиск", on_click=start_search_intersections)
    column_list.append(submit_button)
    check_box_column = ft.Column(spacing=10, controls=column_list, scroll=ft.ScrollMode.ALWAYS, height=900)
    page_row = ft.Row([check_box_column, information_column])
    return page_row


def save_group_users():
    def start_save(e):
        print(group_id)
        try:
            page_column.controls[2] = ft.Text(f"Сохраняем...", size=20)
            page_column.update()
            group_name = SaveGroupUsers(group_id.value, vk_token, host, user, password, database).group_name
            page_column.controls[2] = ft.Text(f"Группа {group_name} сохранена", size=20)
            page_column.update()
        except Error as e:
            page_column.controls[2] = ft.Text(f"Проверьте ID группы", size=20)
            page_column.update()

    group_id = ft.TextField(label="Введите ID группы", hint_text="ID группы")
    submit_to_save_button = ft.ElevatedButton(text="Сохранить", on_click=start_save)
    page_column = ft.Column(spacing=10,
                            controls=[group_id, submit_to_save_button, ft.Text("")],
                            scroll=ft.ScrollMode.ALWAYS,
                            height=900)
    return page_column


def ft_delete_group():
    global groups_count
    groups_count = 0

    def delete_from_screen(group_id):
        for check_box_id in range(2, len(column_list) - 1):
            check_box_group_id = column_list[check_box_id].label.split('"')[3]
            if check_box_group_id == group_id:
                print(group_id)
                column_list.pop(check_box_id)
                print(len(column_list))
                break

    def delete_groups(e):
        global groups_count
        print("Поиск начат")
        groups_to_delete = []
        for line_i in range(len(column_list)):
            group_id = ""
            if 0 < line_i < groups_count + 1:
                if column_list[line_i].value == True:
                    group_id = column_list[line_i].label.split('"')[3]
            if group_id != "":
                groups_to_delete.append(group_id)
        print(groups_to_delete)
        if groups_to_delete:
            for group_id in groups_to_delete:
                DeleteGroupFromBase(group_id, host, user, password, database)
                delete_from_screen(group_id)
                groups_count -= 1
            check_box_column.update()
            print(groups_to_delete, "удален")

    print("экран выбора групп для удаления")
    sql_column = ShowDataBaseTables(host, user, password, database).groups
    column_list = [ft.Text("Выбор группы для удаления")]
    for line in sql_column:
        column_list.append(ft.Checkbox(label=f'"{line[0]}" "{line[1]}"', value=False))
        groups_count += 1
    submit_button = ft.ElevatedButton(text="Удалить", on_click=delete_groups)
    column_list.append(submit_button)
    check_box_column = ft.Column(spacing=10,
                                 controls=column_list,
                                 scroll=ft.ScrollMode.ALWAYS,
                                 height=900)
    return check_box_column
