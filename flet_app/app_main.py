from pages_func import *


def main(page: ft.Page):

    pages = [
        groups_ft_table(),
        search_intersections_screen(),
        save_group_users(),
        ft_delete_group(),
        ft.Text(visible=False,
                size=20,
                color=ft.colors.BLUE,
                spans=[ft.TextSpan(
                    "GitHub проекта!",
                    url="https://github.com/Ifanfomin/vk_analysis_of_users_subscription_to_groups",
                )])
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
                icon=ft.icons.TABLE_ROWS,
                label_content=ft.Text("Список групп")
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.MANAGE_SEARCH,
                label_content=ft.Text("Пересечения")
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.PLAYLIST_ADD,
                label_content=ft.Text("Добавить")
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.PLAYLIST_REMOVE,
                label_content=ft.Text("Удалить")
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.COMMIT,
                label_content=ft.Text("GitHub")
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

ft.app(target=main)
