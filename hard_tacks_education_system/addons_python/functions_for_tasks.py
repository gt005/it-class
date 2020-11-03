from ..models import EducationTask, CheckedEducationTask


def save_task_solution(programm_code: str, programm_code_language: str, request):
    """
    Функция, которая сохраняет решение в таблицу CheckedEducationTask.
    :param programm_code: Код на языке программирования(решение задачи)
    :param programm_code_language: Язык программирования, на котором написан код
    :return: (сообщение с результатом работы, http статус код, task_id)
    """

    if not programm_code:
        return ("Пустой код", 400, None)

    new_solved_task_object = CheckedEducationTask(
        original_task=request.user.puples.educationtask,
        solved_user=request.user.puples,
        task_code=programm_code,
        task_programming_language=programm_code_language,
        contest_token="set_token_here",
        # TODO: Если можно присваивать задаче токен до ее обработки в Яндексе,
        # то записывать тут, иначе поменять поле на null=True
    )

    new_solved_task_object.save()

    return ("Удачно добавлено решение", 200, new_solved_task_object.id)


