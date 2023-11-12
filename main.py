import flet
from flet import *
import json, random, time

with open("tasks.json", "r", encoding="UTF-8") as file:
    tasks: dict = dict(json.load(file))

def main(page: Page):
    page.title = "Теория и вероятность"
    page.vertical_alignment = MainAxisAlignment.CENTER
    time_start = time.time()
    tasks["numbers_def"] = tasks["numbers"]

    def task(e):
        page.controls.clear()
        page.update()

        win_width = int(page.window_width)
        win_height = int(page.window_height)

        task_list: list = tasks["tasks"]
        task_info: dict = task_list[random.randint(0, len(task_list)-1)]
        def test_and_go(e):
            tasks["numbers"] = int(tasks["numbers"]) - 1
            if answer.value in task_info.get("answer"):
                tasks["answer_is_true"] = int(tasks["answer_is_true"]) + 1
            if tasks["numbers"] > 0:
                task("")
            else:
                last_win("")

        answer = TextField(text_size=20, width=win_width-150)
        button = TextButton(text="Далее", width=100, height=70, on_click=test_and_go)

        page.add(
            Text(task_info.get("text"), width=win_width, height=500, size=20),
            TextField(value="Черновик", width=win_width),
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

        page.add(
            Row(
                [
                    Text(
                        f"{tasks['answer_is_true']}/{tasks['numbers_def']}",
                        color=colors.GREEN if tasks['answer_is_true'] >= tasks['answer_is_true_is_good'] else colors.RED)
                ],
                alignment=MainAxisAlignment.CENTER
            ),
            Row(
                [
                    Text(
                        str(int(time.time() - time_start))+" секунд",
                        color=colors.GREEN if int(time.time() - time_start) <= int(tasks["time_is_good_in_second"]) else colors.RED)
                ],
                alignment=MainAxisAlignment.CENTER
            )
        )

    task("")

if __name__ == '__main__':
    flet.app(main)