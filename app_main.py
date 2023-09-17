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
        column =ft.Column(controls=[ft_table], scroll=ft.ScrollMode.ALWAYS, height=900)
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

    pages = [
        groups_ft_table(),
        search_intersections_screen(),
        ft.Text(visible=False,
                color=ft.colors.BLUE,
                spans=[ft.TextSpan(
                    "GitHub проекта!",
                    url="https://github.com/Ifanfomin/vk_analysis_of_users_subscription_to_groups"
                )]),
    ]

    def select_page():
        print(f"Страница {rail.selected_index}")
        for index, p in enumerate(pages):
            p.visible = True if index == rail.selected_index else False
        page.update()

    def dest_change(e):
        select_page()

    page.title = "поиск участников групп вконтакте"


    column = groups_ft_table()  # ft.Column([ft.Text("Body!")], auto_scroll=True)  # alignment=ft.MainAxisAlignment.START, expand=True

    rail = ft.NavigationRail(
        selected_index=1,
        label_type=ft.NavigationRailLabelType.ALL,
        # extended=True,
        min_width=100,
        min_extended_width=0,
        group_alignment=-0.2,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.TABLE_ROWS, label="Список групп"
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.MANAGE_SEARCH,
                label="Пересечения",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.PLAYLIST_ADD,
                label_content=ft.Text("Добавить"),
            ),
        ],
        on_change=dest_change,
    )

    select_page()

    page.window_height = 1080
    page.window_width = 1920

    page.add(
        ft.Row(
            [
                rail,
                ft.VerticalDivider(width=1),
                ft.Row(pages, expand=True, scroll=ft.ScrollMode.ALWAYS)
            ],
            expand=True
        )
    )

    # update_page(column)


ft.app(target=main)
