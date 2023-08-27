import flet as ft
from config import host, user, password, database, vk_token
from classes_main import *

def main(page: ft.Page):
    def groups_ft_table():
        sql_column = ShowDataBaseTables(host, user, password, database).groups
        lines = []
        for line in sql_column:
            data_row = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(line[0])),
                    ft.DataCell(ft.Text(line[1]))
                ]
            )
            lines.append(data_row)

        ft_column = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Имя группы")),
                ft.DataColumn(ft.Text("ID группы"))
            ],
            rows=lines)
        return ft_column

    def search_intersections_screen():
        def make_ft_data_table(users):
            if len(column_list) > 2 + groups_count + 1:
                column_list.pop()
            lines = []
            for user in users:
                data_row = ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(user[0])),
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
                rows=lines)
            column_list.append(ft_table)


        def start_search_intersections(e):
            print("Поиск начат")
            searching_groups = []
            for line_i in range(len(column_list)):
                group_id = ""
                if 1 < line_i < groups_count + 2:
                    if column_list[line_i].value == True:
                        for char in column_list[line_i].label[-2::-1]:
                            if char != '"':
                                group_id += char
                            else:
                                break
                        group_id = group_id[::-1]
                if group_id != "":
                    searching_groups.append(group_id)
            print(searching_groups)
            if searching_groups:
                users = SearchForIntersections(searching_groups, host, user, password, database).users
                print(users)
                make_ft_data_table(users)
                check_box_column.update()

        print("экран выбора групп для поиска пересечений")
        sql_column = ShowDataBaseTables(host, user, password, database).groups
        column_list = [ft.Text(""), ft.Text("Выбор группы для поиска пересечений")]
        groups_count = 0
        for line in sql_column:
            column_list.append(ft.Checkbox(label=f'"{line[0]}" "{line[1]}"', value=False))
            groups_count += 1
        submit_button = ft.ElevatedButton(text="Поиск", on_click=start_search_intersections)
        column_list.append(submit_button)
        check_box_column = ft.Column(spacing=10, controls=column_list, height=400)
        return check_box_column

    def ft_delete_group():
        def delete_from_screen(group_id, groups_count):
            for check_box_id in range(2, len(column_list) - 2):
                check_box_group_id = column_list[check_box_id].label.split('"')[3]
                if check_box_group_id == group_id:
                    print(group_id)
                    column_list.pop(check_box_id)
                    print(len(column_list))
                    check_box_column.update()
                    groups_count -= 1
                    return groups_count

        def delete_groups(e):
            print("Поиск начат")
            groups_to_delete = []
            for line_i in range(len(column_list)):
                group_id = ""
                if 1 < line_i < groups_count + 2:
                    if column_list[line_i].value == True:
                        print(len(column_list))
                        for char in column_list[line_i].label[-2::-1]:
                            if char != '"':
                                group_id += char
                            else:
                                break
                        group_id = group_id[::-1]
                if group_id != "":
                    groups_to_delete.append(group_id)
            print(groups_to_delete)
            if groups_to_delete:
                for group_id in groups_to_delete:
                    # DeleteGroupFromBase(group_id, host, user, password, database)
                    groups_count = delete_from_screen(group_id, groups_count)
                print(groups_to_delete, "удален")

        print("экран выбора групп для удаления")
        sql_column = ShowDataBaseTables(host, user, password, database).groups
        column_list = [ft.Text(""), ft.Text("Выбор группы для удаления")]
        groups_count = 0
        for line in sql_column:
            column_list.append(ft.Checkbox(label=f'"{line[0]}" "{line[1]}"', value=False))
            groups_count += 1
        submit_button = ft.ElevatedButton(text="Удалить", on_click=delete_groups)
        column_list.append(submit_button)
        check_box_column = ft.Column(spacing=10, controls=column_list, height=400)
        return check_box_column

    page.title = "поиск участников групп вконтакте"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = "auto"
    page.window_height = 600
    page.window_width = 800
    # save_group_button = ft.ElevatedButton("Добавить группу в базу", on_click=search_groups_screen)
    # show_groups_button = ft.ElevatedButton("Список групп в базе", on_click=show_groups_screen)
    # delete_group_button = ft.ElevatedButton("Удалить группу из базы", on_click=delete_group_screen)
    # search_intersections_button = ft.ElevatedButton("Поиск пересечений групп", on_click=search_intersections_screen)
    # line_1 = ft.Row(controls=[save_group_button, show_groups_button, delete_group_button, search_intersections_button])
    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Список групп в базе",
                content=groups_ft_table()
            ),
            ft.Tab(
                text="Поиск пересечений групп",
                content=search_intersections_screen()
            ),
            ft.Tab(
                text="Добавить группу в базу",
                content=groups_ft_table()
            ),
            ft.Tab(
                text="Удалить группу из базы",
                content=ft_delete_group()
            )
        ]
    )
    page.add(tabs)
    page.update()

ft.app(target=main)