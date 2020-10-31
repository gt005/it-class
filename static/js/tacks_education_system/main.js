let CookieManager = {
    set: function (name, value, days) {
        let expires = "";
        if (days) {
            let d = new Date();
            d.setTime(d.getTime() + (days * 24 * 60 * 60 * 1000));
            expires = "; expires=" + d.toGMTString();
        }
        document.cookie = name + "=" + value + expires + ";";
        return this.get(name);
    },
    get: function (name) {
        name += "=";
        let b = document.cookie.split(';'), c;
        for (var i = 0; i < b.length; i++) {
            c = b[i].replace(/(^\s+)|(\s+$)/g, "");
            while (c.charAt(0) == ' ')
                c = c.substring(1, c.length);
            if (c.indexOf(name) == 0)
                return c.substring(name.length, c.length);
        }
        return null;
    },
    remove: function (name) {
        this.set(name, "", -1);
    }
};


let lastSolutionsTaskPageSolutionId = 0;


function showAlertElement(message, success = false) {
    // Показывает уведомление на 10 секунд.
    // :param success - true - зеленое, иначе красное.
    let alertElement = `<div class="system-message alert alert-danger alert-dismissible fade show" id="alert-msg" role="alert"><span class="alert-msg-text">${message}</span> <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button> </div>`;

    if (success === true) {
        alertElement = `<div class="system-message alert alert-success alert-dismissible fade show" id="alert-msg" role="alert"><span class="alert-msg-text">${message}</span> <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button> </div>`;
    }

    document.querySelector(".messages-container").innerHTML += alertElement;

    $(".system-message").delay(8000).fadeOut();
}


function convertSecondsToHoursAndMinutes(seconds) {
    // Перевод секунд в часы, минуты и секунды
    if (seconds < 0) {
        seconds = 0;
    }
    let resultTime = ``;
    if (Math.trunc(seconds / 86400 / 7) !== 0) {
        resultTime += `${Math.trunc(seconds / 86400 / 7)} нед `
    }
    if (Math.trunc(seconds % 604800 / 86400) !== 0) {
        resultTime += `${Math.trunc(seconds % 604800 / 86400)} дн `
    }
    if (Math.trunc(seconds % 86400 / 3600) !== 0) {
        resultTime += `${Math.trunc(seconds % 86400 / 3600)} ч `
    }
    if (Math.trunc(seconds % 3600 / 60) !== 0) {
        resultTime += `${Math.trunc(seconds % 3600 / 60)} мин `
    }
    if (Math.trunc(seconds % 60) !== 0) {
        resultTime += `${seconds % 60} сек`
    }

    return resultTime
}


function deleteTaskPageInsertCodeArea() {
    // Удаленеи поля с кодом
    let codeSection = document.querySelector(".task-page__insert-code .container");
    $(codeSection).slideUp('slow');
}


function changeLastSolutionTaskPage(solutionTime, codeLang, solutionCode) {
    /* Изменяет таблицу с последним решение,
     если она пустая, то добавляется запись,
      иначе обновляется надписи последней записи
    */

    let lastSolutionRow = `<div class="card task-page__last-solutions__card">
                                <div class="card-header" id="heading${lastSolutionsTaskPageSolutionId}">
                                    <h2 class="mb-0">
                                        <button class="btn btn-block text-left collapsed"
                                                type="button"
                                                data-toggle="collapse"
                                                data-target="#collapse${lastSolutionsTaskPageSolutionId}"
                                                data-code=""
                                                aria-expanded="false"
                                                aria-controls="collapse${lastSolutionsTaskPageSolutionId}">
                                            <span class="task-page__last-solutions__table__body__row">
                                                <span class="task-page__last-solutions__table__body__row__time">
                                                    ${solutionTime}
                                                </span>
                                                <span class="task-page__last-solutions__table__body__row__lang">
                                                    ${codeLang}
                                                </span>
                                            </span>
                                        </button>
                                    </h2>
                                </div>
                                <div id="collapse${lastSolutionsTaskPageSolutionId}" class="collapse"
                                     aria-labelledby="heading${lastSolutionsTaskPageSolutionId}"
                                     data-parent="#accordionExample">
                                    <div class="card-body task-page__last-solutions__table__body__row__show-code-area">
                                        <pre>${solutionCode}</pre>
                                    </div>
                                </div>
                            </div>`

    let lastSolutionSection = document.querySelector('.task-page__last-solutions'),
        lastSolutionTable = document.querySelector('.task-page__last-solutions__table'),
        lastSolutionTableBody = document.querySelector('.task-page__last-solutions__table__body');

    if (lastSolutionTableBody.textContent === '') {
        $(lastSolutionSection).fadeIn('slow');
        $(lastSolutionTable).fadeIn('slow');
    }

    lastSolutionTableBody.innerHTML = lastSolutionRow + lastSolutionTableBody.innerHTML;
    lastSolutionsTaskPageSolutionId++;
}


function sendTaskSolution(fileOrCodeText, codeLang, type) {

    let csrfToken = document.querySelector('#task-page__code-tabs-content input[name="csrfmiddlewaretoken"]').value,
        codeAreaLoader = document.querySelector(".task-page__insert-code__loader"),
        codeToAddToLastSolution = '';

    codeAreaLoader.style = 'opacity: 1;visibility: visible;';

    let data = new FormData();
    if (type === 'code') {
        data.append('taskSolutionType', 'code');
        codeToAddToLastSolution = fileOrCodeText;
        data.append('codeText', fileOrCodeText);
    } else if (type === 'file') {
        data.append('taskSolutionType', 'file');
        data.append('taskSolutionFile', fileOrCodeText);
    }
    data.append('codeLang', codeLang);

    fetch(location.href, {
        method: 'POST',
        headers: {"X-CSRFToken": csrfToken},
        body: data
    }).then(function (response) {
        if (!response.ok) {
            showAlertElement('Произошла ошибка, попробуйте перезагрузить страницу');
            codeAreaLoader.style = 'opacity: 0;visibility: hidden;';
            return false
        }
        return response.json();
    }).then(function (json) {
        if (json) {
            if (codeToAddToLastSolution === '') {
                codeToAddToLastSolution = json.solutionCode;
            }
            changeLastSolutionTaskPage(
                json.solutionTime,
                codeLang,
                codeToAddToLastSolution,
            )
            showAlertElement("Задача отправлена!" + json.message, true);
            codeAreaLoader.style = 'opacity: 0;visibility: hidden;';
        }
    });
}


function remainderTimeCounter(
    target, message_on60_seconds,
    function_on_end=undefined,
    message_type = false,
    red_color_toggle = true,
    set_red_end_message = true,
    end_message_alert = undefined,
    end_message_alert_type=false,
) {
    /* target - Объект с количеством секунд в виде числа.
    *  function_on_end - функция, выполняемая при окончании времени.
    *  red_color_toggle - boolean, должено ли время мигать, когда остается 60 секунд.
    *  message_on60_seconds - Сообщение, которое должно быть показано, когда остается 60 секунд.
    *  message_type - boolean, false - выводится красное сообщение на 60 секунд, иначе зеленое.
    *  set_red_end_message - Заменять ли время на красную надпись "Время закончилось".
    *  end_message_alert - Сообщение, которое покажется сверху экрана как уведомление, когда закончится время. Если не задано, то "Время вышло!".
    *  end_message_alert_type - boolean, false - выводится красное сообщение при окончании времени, иначе зеленое.
    *  */
    let targetSeconds = target.textContent;
    target.textContent = convertSecondsToHoursAndMinutes(target.textContent);  // Перевод в читаемый вид из секунд сразу после загрузки скрипта

    let remainderTimeInterval = setInterval(() => {
        // Счетчик времени на странице с задачей
        targetSeconds--;
        target.textContent = convertSecondsToHoursAndMinutes(targetSeconds);
        if (targetSeconds <= 0) {

            if (set_red_end_message) {
                target.textContent = "Время закончилось";
                target.style.color = 'red';
            }

            if (end_message_alert === undefined) {
                showAlertElement("Время вышло!", end_message_alert_type);
            } else {
                showAlertElement(end_message_alert, end_message_alert_type);
            }

            if (function_on_end){
                function_on_end();
            }
            clearCurrentInterval();
        } else if (targetSeconds <= 60 && red_color_toggle) {
            if (targetSeconds % 2 === 0) {
                target.style.color = 'red';
            } else {
                target.style.color = 'black';
            }
        }
        if (targetSeconds == 60) {
            showAlertElement(message_on60_seconds, message_type);
        }
    }, 1000);

    function clearCurrentInterval () {
        clearInterval(remainderTimeInterval);
    }
}
