import datetime

from django.http import JsonResponse

from ..models import EducationTask, CheckedEducationTask, EducationLevel


def crete_level(level_number: int, level_theme: str) -> (str, int):
    """
    Создает уровень с темой.
    :param level_number: Номер уровня, который создать.
     Должен быть следующим после существуещего.
    :param level_theme: Тема уровня.
    :return: tuple(Сообщение, http статус код)
    """
    last_exist_level = EducationLevel.objects.all()
    if last_exist_level:
        last_exist_level = last_exist_level.order_by("-level_number")[0]
    else:
        last_exist_level = 0

    try:
        level_number = int(level_number)
    except ValueError:
        return (
            "Уровень не является числом",
            400
        )

    if last_exist_level.level_number + 1 != level_number:
        return (
            "Уровень не является следующим",
            400
        )

    if len(str(level_theme)) > 255 or len(str(level_theme)) < 3:
        return (
            "Название уровня больше 255 символов или меньше 3",
            400
        )

    EducationLevel(level_number=level_number, level_theme=level_theme).save()
    return (
        "Уровень успешно создан.",
        200
    )


def create_solution_task_db_object(programm_code: str, programm_code_language: str, request):
    """
    Функция, которая сохраняет решение в таблицу CheckedEducationTask.
    :param programm_code: Код на языке программирования(решение задачи)
    :param programm_code_language: Язык программирования, на котором написан код
    :return: (сообщение с результатом работы, http статус код, task_id)
    """

    active_task = request.user.puples.educationtask
    if not (active_task.end_time >= datetime.datetime.now() >= active_task.start_time):
        return ("Задача не активна", 403, None)

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


def save_task_solution(request) -> JsonResponse:
    """
    Производит проверки на валидность и сохраняет задачу в базе данных.
    """
    solution_task_time = ''
    existing_programming_languages = {
        "Python 3.7.3",
        "GNU C11 7.3",
        "GNU c++17 7.3"
    }
    if request.POST.get("codeLang") not in existing_programming_languages:
        return JsonResponse({
            "message": "Неправильный язык программирования",
        }, status=400)

    if request.POST.get("taskSolutionType") == "code":
        result_message, http_code, task_id = create_solution_task_db_object(
            programm_code=request.POST.get("codeText"),
            programm_code_language=request.POST.get("codeLang"),
            request=request
        )

        if task_id is not None:
            solution_task_time = CheckedEducationTask.objects.get(
                id=task_id
            ).get_solution_time()

        return JsonResponse({
            "message": result_message,
            "solutionTime": solution_task_time,
            "solutionId": task_id
        }, status=http_code)

    elif request.POST.get("taskSolutionType") == "file":

        try:
            file_code = request.FILES.get(
                "taskSolutionFile").open().read().decode("utf-8")
        except TypeError:
            return JsonResponse({
                "message": "Пустой файл",
            }, status=400)

        result_message, http_code, task_id = create_solution_task_db_object(
            programm_code=file_code,
            programm_code_language=request.POST.get("codeLang"),
            request=request
        )

        if task_id is not None:
            solution_task_time = CheckedEducationTask.objects.get(
                id=task_id
            ).get_solution_time()

            return JsonResponse({
                "message": result_message,
                "solutionTime": solution_task_time,
                "solutionCode": file_code,
                "solutionId": task_id
            }, status=http_code)
    return JsonResponse({
        "message": "Задача не подходит ни под один тип решения."
    }, status=400)
