import datetime
from random import shuffle, choice

from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect

from typing import Any, Optional

from ..models import EducationTask, CheckedEducationTask, EducationLevel
from mainapp.models import Puples


def sort_list_with_none(element: int) -> int:
    """ Функция-ключ для сортировки чисел с None """
    if element is None:
        return 0
    return element


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

    people_amount_with_current_level = get_amount_of_people_with_level(level_number)

    if people_amount_with_current_level != 0:
        percents = round(tasks_amount / people_amount_with_current_level * 100)
        if percents > 100:
            return 100
        return percents
    return 0


def get_level_average_score(level_object_from_db: EducationLevel) -> int:
    ''' Возвращает средний балл по уровню от 0 до 300 '''
    all_solved_tasks = CheckedEducationTask.objects.all()

    tasks_score_sum = 0
    tasks_amount = 0

    for solved_task in all_solved_tasks:
        if solved_task.original_task.task_level == level_object_from_db and \
                solved_task.result_summ_mark is not None:
            tasks_amount += 1
            tasks_score_sum += solved_task.result_summ_mark

    if tasks_amount != 0:
        return int(tasks_score_sum / tasks_amount)
    else:
        return -1


def get_max_student_level() -> int:
    """ Возвращает самый высокий уровень среди учеников """
    return max(
        Puples.objects.all(),
        key=lambda student: student.education_level
    ).education_level


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
        request_object,
        level_object_from_db: EducationTask) -> JsonResponse:
    """
    Создает задачу для определенного уровня и добавляет ее в базу данных.
    :param post_request_object: объект post запроса пользователя (dict).
    :return: JsonResponse
    """
    post_request_object = request_object.POST

    start_time = datetime.datetime.strptime(post_request_object.get("start_time"), "%d %B %Y г. %H:%M")
    end_time = datetime.datetime.strptime(post_request_object.get("end_time"), "%d %B %Y г. %H:%M")

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
        photo_1=request_object.FILES.get("photo_1"),
        photo_2=request_object.FILES.get("photo_2"),
        photo_3=request_object.FILES.get("photo_3"),
        example_input_1=post_request_object.get("example_input_1"),
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


def is_all_tasks_ends_on_level(level_number: int) -> bool:
    """ Возвращает, закрылись ли все задачи уровня """
    level_object_from_db = get_object_from_db(
        database=EducationLevel,
        object_parameters={'level_number': level_number}
    )

    list_of_tasks = list(EducationTask.objects.filter(
        task_level=level_object_from_db
    ))

    for task in list_of_tasks:
        if task.for_student is not None:
            if datetime.datetime.now() < task.end_time:
                return False
    return True


def direct_levels_tasks_to_estimate(request) -> None:
    """ Отправляет все задачи на проверку уровня, на котором ученик.
        Отправляет, если все задачи уже нельзя сдавать.
    """
    level_object_from_db = get_object_from_db(
        database=EducationLevel,
        object_parameters={'level_number': request.user.puples.education_level}
    )

    list_of_tasks = list(EducationTask.objects.filter(
        task_level=level_object_from_db
    ))

    # Закончилось ли время решения всех задач
    is_all_tasks_closed = is_all_tasks_ends_on_level(request.user.puples.education_level)

    if is_all_tasks_closed:
        list_of_students = list(Puples.objects.filter(
            education_level=level_object_from_db.level_number
        ))
        shuffle(list_of_students)

        # Первый peer
        for i in range(len(list_of_students)):
            list_of_students[i].first_peer = list_of_students[
                (i + 1) % len(list_of_students)
            ]
            list_of_students[i].first_peer = list_of_students[
                (i + 3) % len(list_of_students)
            ]


def check_existing_active_task(delete_for_user: Puples) -> bool:
    '''
    Удаляет активную задачу у ученика(убирает привязку),
     если время ее сдачи вышло.
    :param delete_for_user: Для ученика, для которого делать проверку.
    :return: True, если задача остается и ее не удалило или не существует, иначе False
    '''
    try:
        if datetime.datetime.now() > delete_for_user.educationtask.end_time:
            task = get_object_from_db(
                database=EducationTask,
                object_parameters={'for_student': delete_for_user}
            )
            task.for_student = None
            task.save()
            return False
        return True
    except Exception as expt:  # RelatedObjectDoesNotExist
        print(expt)
        return False


def get_object_from_db(database, object_parameters: dict) -> Optional[Any]:
    '''
    Функция осуществляет поиск по базе данных не вызывая
    исключений при отсутствии объекта.

    :param database: таблица в базе данных в которой искать (передавать объектом бд)
    :param object_parameters: словарь фильтров, по которым искать запись
    :return: Возвращает запись из таблицы если запись существует, иначе None
    '''
    try:
        return database.objects.get(**object_parameters)
    except ObjectDoesNotExist:
        return


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


def change_task_data_in_model(
        request_object, for_task: EducationTask) -> JsonResponse:
    """ Изменяет данные задачи из формы """

    post_request_object = request_object.POST

    for_task.task_name = post_request_object.get("task_name_edit")
    for_task.description_task = post_request_object.get("description_task_edit")
    for_task.input_format = post_request_object.get("id_input_format_edit")
    for_task.output_format = post_request_object.get("output_format_edit")

    if request_object.FILES.get("photo_1") is not None:
        for_task.photo_1 = request_object.FILES.get("photo_1")
    elif post_request_object.get("is_photo_1_deleted") == "true":
        for_task.photo_1 = None

    if request_object.FILES.get("photo_2") is not None:
        for_task.photo_2 = request_object.FILES.get("photo_2")
    elif post_request_object.get("is_photo_2_deleted") == "true":
        for_task.photo_2 = None

    if request_object.FILES.get("photo_3") is not None:
        for_task.photo_3 = request_object.FILES.get("photo_3")
    elif post_request_object.get("is_photo_3_deleted") == "true":
        for_task.photo_3 = None

    for_task.example_input_1 = post_request_object.get("example_input_1_edit")
    for_task.example_output_1 = post_request_object.get("example_output_1_edit")
    for_task.example_input_2 = post_request_object.get("example_input_2_edit")
    for_task.example_output_2 = post_request_object.get("example_output_2_edit")
    for_task.example_input_3 = post_request_object.get("example_input_3_edit")
    for_task.example_output_3 = post_request_object.get("example_output_3_edit")

    for_task.save()

    return redirect(f"/tasks/system_settings/level-settings/{for_task.task_level.level_number}")


def distribute_tasks_among_students(level_number: int) -> JsonResponse:
    '''
    Распределяет задачи среди учеников данного уровня.
    Для каждого ученика не может повторяться задача, НО
    если задач, которые ученик не решал не осталось, то выбирается случацная
    задача.
    Распределение будет происходить только если для каждого ученика есть задача.
    :param level_number: Уровень, для которого распределить задачи.
    :return: True, если распределение произошло, иначе False.
    '''
    if get_level_fullness_percents(level_number) < 100:
        return JsonResponse(
            {"message": "Не для каждого ученика есть задача"},
            status=400
        )

    level_object_from_db = get_object_from_db(
        database=EducationLevel,
        object_parameters={'level_number': level_number}
    )

    if level_object_from_db is None:
        return JsonResponse(
            {"message": "Уровня не существует"},
            status=404
        )

    list_of_students = list(Puples.objects.filter(
        education_level=level_object_from_db.level_number
    ))
    list_of_tasks = list(EducationTask.objects.filter(
        task_level=level_object_from_db
    ))
    remaining_students = []  # Ученики, которые решили все задачи уровня

    shuffle(list_of_tasks)

    # Обнуление, чтобы не было конфлика pk
    for task in list_of_tasks:
        task.for_student = None
        task.for_student_id = None
        task.save()

    for student in list_of_students:
        solved_tasks_for_student = CheckedEducationTask.objects.filter(  # Решенные задачи
            solved_user=student
        )

        is_task_found = False  # Если ученик уже прорешал все задачи этого уровня, то ему выдаст оставшуюся задачу в конце
        for task_index, possible_task in enumerate(list_of_tasks):
            is_solved_task = False

            # Проверка на то, что ученик еще не решал такую задачу
            for checked_task in solved_tasks_for_student:
                if possible_task == checked_task.original_task:
                    is_solved_task = True  # Нашлась в списке решений
                    break

            if not is_solved_task:
                possible_task.for_student = student
                possible_task.for_student_id = student.id
                possible_task.save()
                is_task_found = True
                list_of_tasks.pop(task_index)
                break

        if not is_task_found:
            remaining_students.append(student)

    # Распределение оставшихся студентов
    for remained_student in remaining_students:
        list_of_tasks[0].for_student = remained_student
        list_of_tasks[0].save()
        list_of_tasks.pop(0)

    return redirect(f"/tasks/system_settings/level-settings/{level_number}")


def set_time_to_all_level_tasks(level: EducationLevel,
                                start_time: str,
                                end_time: str) -> JsonResponse:
    """ Задает время открытия и закрытия задач для всех задач уровня """
    start_time = datetime.datetime.strptime(start_time, "%d %B %Y г. %H:%M")
    end_time = datetime.datetime.strptime(end_time, "%d %B %Y г. %H:%M")

    if end_time <= start_time:
        return JsonResponse(
            {"message": "Конечное время раньше начального."},
            status=400
        )

    level_tasks_list_from_db = EducationTask.objects.filter(
        task_level=level
    )

    for task in level_tasks_list_from_db:
        task.start_time = start_time
        task.end_time = end_time
        task.save()

    return JsonResponse(
            {"message": "Время успешно установлено."},
            status=200
        )


def distribute_tasks_for_estimate() -> None:
    """ Распределяет задачи на оценку между учениками """
    max_student_level = get_max_student_level()
    solved_tasks_list = []
    all_users_lst = Puples.objects.all()
    students_list = list(filter(
        lambda people: not people.user.is_superuser,
        all_users_lst
    ))
    teachers_list = list(filter(
        lambda people: people.user.is_superuser,
        all_users_lst
    ))

    for level_number in range(1, max_student_level + 1):
        level_object_from_db = get_object_from_db(
            database=EducationLevel,
            object_parameters={
                'level_number': level_number}
        )

        if not is_all_tasks_ends_on_level(level_number):
            continue

        solved_tasks_list += list(filter(
            lambda task: task.original_task.task_level == level_object_from_db,
            CheckedEducationTask.objects.filter(
                first_peer=None,
                second_peer=None
            )
        ))
    for solved_task in solved_tasks_list:
        # Поиск первого пира
        shuffle(students_list)
        for first_peer in students_list:
            if first_peer != solved_task.solved_user and \
                    solved_task.task_programming_language in first_peer.task_education_addition_data['known_languages']:
                solved_task.first_peer = first_peer
                break
        # Поиск второго пира
        for second_peer in students_list:
            if second_peer != solved_task.solved_user and \
                    solved_task.task_programming_language in second_peer.task_education_addition_data['known_languages'] and \
                    second_peer != first_peer:
                solved_task.second_peer = second_peer
                break

        if solved_task.first_peer is None:
            solved_task.first_peer = choice(teachers_list)

        if solved_task.second_peer is None:
            solved_task.second_peer = choice(teachers_list)

        solved_task.save()


def set_estimate_rate(request_object) -> None:
    """ Задает оценку задачи от пира """
    task_to_set_estimate: CheckedEducationTask = CheckedEducationTask.objects.filter(
        id=int(request_object.POST.get("task_id"))
    )

    if task_to_set_estimate:
        task_to_set_estimate = task_to_set_estimate[0]

    print()
    print(task_to_set_estimate.first_peer_mark, task_to_set_estimate.second_peer_mark)
    print()

    if task_to_set_estimate.first_peer == request_object.user.puples:
        task_to_set_estimate.first_peer_mark = request_object.POST.get("task_score")
    if task_to_set_estimate.second_peer == request_object.user.puples:
        task_to_set_estimate.second_peer_mark = request_object.POST.get("task_score")

    if task_to_set_estimate.first_peer_mark is not None and \
            task_to_set_estimate.second_peer_mark is not None:
        print("Вызов функции отправки в Яндекс Контест")

    task_to_set_estimate.save()


def get_student_statistic(request_object) -> JsonResponse:
    """ Возвращает набор статистики для страницы Students Statistic для учителя """
    student_from_db = get_object_from_db(
        database=Puples,
        object_parameters={
            "id": request_object.POST.get("get_data_from_user_id")
        }
    )

    if student_from_db is None:
        return JsonResponse({
            "message": "Ученик не найден"
        }, status=404)

    return JsonResponse({
        "tasksList": list(map(
            lambda task: str(task),
            CheckedEducationTask.objects.filter(
            solved_user=student_from_db
        )))
    }, status=200)


