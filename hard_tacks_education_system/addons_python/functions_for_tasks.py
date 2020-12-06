import datetime

from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from ..models import EducationTask, CheckedEducationTask, EducationLevel
from mainapp.models import Puples


def get_amount_of_people_with_level(level_number: int) -> int:
    """ Возвращает количество учеников у которых определенный уровень """
    try:
        return len(Puples.objects.filter(education_level=level_number))
    except (ObjectDoesNotExist, TypeError, ValueError):
        return 0


def get_level_fullness_percents(level_number: int) -> int:
    """ Возвращает процент заполнености уровня задачами (Задачи / Ученики) """
    try:
        task_level = EducationLevel.objects.get(
            level_number=level_number
        )
        tasks_amount = len(EducationTask.objects.filter(
            task_level=task_level
        ))
    except (TypeError, ValueError, ObjectDoesNotExist):
        return 0

    if tasks_amount != 0:
        percents = round(tasks_amount / get_amount_of_people_with_level(level_number) * 100)
        if percents > 100:
            return 100
        return percents
    return 0


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


def create_solution_task_db_object(
        programm_code: str,
        programm_code_language: str,
        request
) -> (str, int, int):
    """
    Функция, которая сохраняет решение в таблицу CheckedEducationTask.
    :param programm_code: Код на языке программирования(решение задачи)
    :param programm_code_language: Язык программирования, на котором написан код
    :return: (сообщение с результатом работы, http статус код, task_id)
    """

    active_task = request.user.puples.educationtask
    if not (
            active_task.end_time >= datetime.datetime.now() >= active_task.start_time):
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


def delete_task_solutions_except_last(
        last_solution_id: int,
        user: Puples) -> None:
    """ Удаляет все решения конкретной задачи, кроме данной """
    original_task = CheckedEducationTask.objects.get(
        id=last_solution_id
    ).original_task

    last_tasks = CheckedEducationTask.objects.filter(
        original_task=original_task,
        solved_user=user
    ).exclude(
        id=last_solution_id
    )

    for task_for_delete in last_tasks:
        task_for_delete.delete()


def save_task_last_solution(request) -> JsonResponse:
    """
    Производит проверки на валидность и сохраняет задачу в базе данных.
    При этом удаляет прошлые решения
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

        delete_task_solutions_except_last(
            last_solution_id=task_id,
            user=request.user.puples
        )
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

            delete_task_solutions_except_last(
                last_solution_id=task_id,
                user=request.user.puples
            )
            return JsonResponse({
                "message": result_message,
                "solutionTime": solution_task_time,
                "solutionCode": file_code,
                "solutionId": task_id
            }, status=http_code)
    return JsonResponse({
        "message": "Задача не подходит ни под один тип решения."
    }, status=400)


def change_level_theme(new_theme: str,
                       for_level: EducationTask) -> JsonResponse:
    """
    Изменяет тему уровня.
    :param new_theme: Тему, на которую надо изменить
    :param for_level: Для какого уровня изменять тему
    :return: JsonResponse
    """

    if not (3 <= len(new_theme) <= 255):
        return JsonResponse({
            "message": "Неправильная длина новой темы"
        }, status=400)

    for_level.level_theme = new_theme
    for_level.save()

    return JsonResponse({
        "message": "Успещно сменена тема"
    }, status=200)


def create_task_and_add_to_db(
        post_request_object: dict,
        level_object_from_db: EducationTask) -> JsonResponse:
    """
    Создает задачу для определенного уровня и добавляет ее в базу данных.
    :param post_request_object: объект post запроса пользователя (dict).
    :return: JsonResponse
    """

    print(post_request_object.get("task_name"))

    start_time = _get_datetime_time_object_from_string(
        string_to_convert=post_request_object.get("start_time")
    )
    end_time = _get_datetime_time_object_from_string(
        string_to_convert=post_request_object.get("end_time")
    )

    if end_time <= start_time:
        print("Некорректные даты")
        return JsonResponse({
            "message": "Некорректные даты"
        }, status=400)

    new_task_object = EducationTask(
        start_time=start_time,
        end_time=end_time,
        task_level=level_object_from_db,
        task_name=post_request_object.get("task_name"),
        description_task=post_request_object.get("description_task"),
        input_format=post_request_object.get("input_format"),
        output_format=post_request_object.get("output_format"),
        photo_1=post_request_object.get("photo_1"),
        photo_2=post_request_object.get("photo_2"),
        photo_3=post_request_object.get("photo_3"),
        example_input_1=post_request_object.get("photo_1"),
        example_output_1=post_request_object.get("example_output_1"),
        example_input_2=post_request_object.get("example_input_2"),
        example_output_2=post_request_object.get("example_output_2"),
        example_input_3=post_request_object.get("example_input_3"),
        example_output_3=post_request_object.get("example_output_3"),
    )

    new_task_object.save()
    return JsonResponse({
        "message": "Задача успешно создана",
        "task_id": new_task_object.id,
    }, status=200)


def check_existing_active_task(delete_for_user: Puples) -> bool:
    '''
    Удаляет активную задачу у ученика(убирает привязку),
     если время ее сдачи вышло.
    :param delete_for_user: Для ученика, для которого делать проверку.
    :return: True, если задача остается и ее не удалило или не существует, иначе False
    '''
    try:
        if datetime.datetime.now() > delete_for_user.educationtask.end_time:
            delete_for_user.educationtask.for_student = None
            delete_for_user.educationtask = None
            delete_for_user.save()
            delete_for_user.educationtask.save()
            return False
        return True
    except:  # RelatedObjectDoesNotExist
        return False


def try_to_get_object_from_db(database, object_parameters):
    '''
    Функция осуществляет поиск по базе данных не вызывая
    исключений при отсутствии объекта.

    :param database: таблица в базе данных в которой искать (передавать объектом бд)
    :param object_parameters: список фильтров, по которым искать запись
    :return: Возвращает запись из таблицы если запись существует, иначе None
    '''
    pass


def delete_task_from_db(task_id: int) -> JsonResponse:
    ''' Удаляет задачу из базы данных '''
    try:
        EducationTask.objects.get(id=task_id).delete()
    except ObjectDoesNotExist:
        return JsonResponse({
            "message": "Нет такой задачи"
        }, status=404)
    except TypeError:
        return JsonResponse({
            "message": "Некорректный id"
        }, status=400)

    return JsonResponse({
        "message": "Задача успешно удалена"
    }, status=200)


def change_task_data_in_model(request) -> JsonResponse:
    """ Изменяет данные задачи из формы """
    pass


def _get_datetime_time_object_from_string(string_to_convert: str):
    """
    Переводить строку формата 'month/day/year hour:minutes' в объект datetime
    :param string_to_convert: Строка, из которой сделать объект datetime
    :return: datetime object
    """

    result_time = datetime.datetime.strptime(
        str(string_to_convert[:-3]),
        "%m/%d/%Y %I:%M"
    )

    if string_to_convert.endswith('PM'):
        result_time += datetime.timedelta(hours=12)

    return result_time
