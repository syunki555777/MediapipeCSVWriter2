import flet as ft

def screen():

    def movies():
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.ALBUM),
                            title=ft.Text("動画のタイトル"),
                            subtitle=ft.Text(
                                "変換中"
                            ),
                        ),
                        ft.Row(
                            [ft.TextButton("中断"), ft.TextButton("詳細")],
                            alignment=ft.MainAxisAlignment.END,
                        ),
                    ]
                ),
                padding=10,
            )
        )
    waitList = ft.Column(
        scroll=ft.ScrollMode.ALWAYS,
        height=300,
    )
    nowProcess = movies()
    waitList.controls.append(movies())
    waitList.controls.append(movies())
    waitList.controls.append(movies())

    page = ft.Column(
        [
        ft.Text(value="処理中"),
        nowProcess,
        ft.Text(value="待機中"),
            ft.Container(
                content=waitList,
                expand=True,
            ),
        ]
    )
    return page
