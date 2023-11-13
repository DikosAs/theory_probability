import flet
from flet import *
import json, random, time

with open("tasks.json", "r", encoding="UTF-8") as file:
    tasks: dict = dict(json.load(file))

def main(page: Page):
    page.title = "Тренажер для подготовки к ЕГЭ по математике"
    page.theme_mode = ThemeMode.LIGHT
    time_start = time.time()
    tasks["numbers_def"] = tasks["numbers"]

    def task(e):
        page.controls.clear()
        page.update()

        win_width = int(page.window_width)
        win_height = int(page.window_height)

        task_list: list = tasks["tasks"]
        taskID = random.randint(0, len(task_list)-1)
        task_info: dict = task_list[taskID]
        del tasks.get("tasks")[taskID]

        def test_and_go(e):
            tasks["numbers"] = int(tasks["numbers"]) - 1
            tasks["answer_is_true"][str(int(tasks["numbers_def"]) - int(tasks["numbers"]))] = "1" if answer.value.replace(".", ",") == task_info.get("answer") else "0"
            if tasks["numbers"] > 0:
                task("")
            else:
                last_win("")

        answer = TextField(text_size=20, width=win_width-150, label="Ответ")
        button = TextButton(text="Далее", width=100, height=70, on_click=test_and_go)

        page.add(
            Row([Text("Тренажёр по математике", size=50)], alignment=MainAxisAlignment.CENTER),
            Divider(height=10, thickness=5, color=colors.RED),
            Row(
                [
                    VerticalDivider(color=colors.BLACK, thickness=2),
                    Column([
                        Text(task_info.get("text"), width=1200, height=350, size=20),
                        Text("Ответ округлите до сотых", width=1200, height=50, size=20)
                    ]),
                    VerticalDivider(color=colors.BLACK, thickness=2)
                ],
                alignment=MainAxisAlignment.CENTER,
                spacing=0,
                expand=True
            ),
            TextField(label="Черновик", width=win_width),
            Row(
                [
                    answer,
                    button
                ]
            )
        )

        page.update()

    def last_win(e):
        page.controls.clear()
        page.update()
        page.vertical_alignment = MainAxisAlignment.CENTER

        for number in tasks["answer_is_true"].keys():
            taskID = number
            icon = icons.CHECK_BOX if tasks["answer_is_true"][number] == "1" else icons.INDETERMINATE_CHECK_BOX
            page.add(
                Row(
                    [
                        Text(f"{taskID}:", size=30),
                        Icon(icon, color=colors.GREEN if tasks["answer_is_true"][number] == "1" else colors.RED, size=30)
                    ],
                    alignment=MainAxisAlignment.CENTER
                )
            )

        time_work = int(time.time() - time_start)
        minutes = time_work//60
        seconds = time_work-(time_work//60*60)
        seconds = seconds if seconds >= 10 else f"0{seconds}"
        color = colors.YELLOW if minutes < 6 else colors.GREEN if minutes > 6 and (minutes < 7 or (minutes == 7 and int(seconds) == 0)) else colors.RED

        page.add(
            Row(
                [
                    Text(
                        f"{minutes}:{seconds}",
                        color=colors.BLACK,
                        size=30
                    )
                ],
                alignment=MainAxisAlignment.CENTER
            ),
        Row(
            [
                Text(
                    f"Для 5 задач норма по времени 6-7 минут",
                    color=colors.BLACK,
                    size=30
                )
            ],
            alignment=MainAxisAlignment.CENTER
        )
        )

    task("")

if __name__ == '__main__':
    flet.app(main)