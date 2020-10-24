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
    if (Math.trunc(seconds / 3600) !== 0) {
        resultTime += `${Math.trunc(seconds / 3600)} ч `
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

    console.log(solutionTime);

    const lastSolutionRow = `<tr class="task-page__last-solutions__table__body__row">
                                <td class="task-page__last-solutions__table__body__row__time">${solutionTime}</td>
                                <td class="task-page__last-solutions__table__body__row__lang">${modeToLang[codeLang]}</td>
                                <td class="task-page__last-solutions__table__body__row__show-code">
                                    Посмотреть код
                                </td>
                            </tr>`

    let lastSolutionSection = document.querySelector('.task-page__last-solutions'),
        lastSolutionTable = document.querySelector('.task-page__last-solutions__table'),
        lastSolutionTableRowTime = document.querySelector('.task-page__last-solutions__table__body__row__time'),
        lastSolutionTableRowLang = document.querySelector('.task-page__last-solutions__table__body__row__lang'),
        lastSolutionCodeArea = document.querySelector('.task-page__last-solutions__table__body__row__show-code-area pre'),
        lastSolutionTableBody = document.querySelector('.task-page__last-solutions__table__body');

    if (lastSolutionTableBody.textContent === '') {
        $(lastSolutionSection).fadeIn('slow');
        $(lastSolutionTable).fadeIn('slow');
        lastSolutionTableBody.innerHTML = lastSolutionRow;
    } else {
        lastSolutionTableRowTime.textContent = solutionTime;
        lastSolutionTableRowLang.textContent = modeToLang[codeLang];
    }

    lastSolutionCodeArea.textContent = solutionCode;

    let openCodeButton = document.querySelector('.task-page__last-solutions__table__body__row__show-code'),
        lastCode = document.querySelector('.task-page__last-solutions__table__body__row__show-code-area');
    // Работа с таблицей после задачи(на предыдущие отправки)
    openCodeButton.onclick = function () {
        $(lastCode).fadeToggle('slow');
    }
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

    fetch(`${location.origin}/tasks/active_task/`, {
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
            changeLastSolutionTaskPage(json.solutionTime, codeLang, codeToAddToLastSolution)
            showAlertElement("Задача отправлена!" + json.message, true);
            codeAreaLoader.style = 'opacity: 0;visibility: hidden;';
        }
    });
}

// Страница с задачей
let remainderTime = document.querySelector("#task-page__time-remainder__time"),
    remainderTimeStartSeconds = remainderTime.textContent,
    taskPageCodeSection = document.querySelector(".task-page__insert-code"),
    taskPageTimeEndLabel = document.querySelector('.task-page__insert-code__time-end-label'),
    expansionToMode = {
        'py': 'python',
        'c': 'text/x-csrc',
        'cpp': 'text/x-c++src'
    },
    modeToLang = {
        'python': 'Python 3.7.3',
        'text/x-csrc': 'GNU c++17 7.3',
        'text/x-c++src': 'GNU C11 7.3'
    };

remainderTime.textContent = convertSecondsToHoursAndMinutes(remainderTimeStartSeconds);

let remainderTimeInterval = setInterval(() => {
    // Счетчик времени на странице с задачей
    remainderTimeStartSeconds--;
    remainderTime.textContent = convertSecondsToHoursAndMinutes(remainderTimeStartSeconds);
    if (remainderTimeStartSeconds <= 0) {

        remainderTime.textContent = "Время закончилось";
        remainderTime.style.color = 'red';
        showAlertElement("Время вышло!");

        deleteTaskPageInsertCodeArea();
        $(taskPageTimeEndLabel).fadeIn('slow');

        clearInterval(remainderTimeInterval);
    } else if (remainderTimeStartSeconds <= 60) {
        if (remainderTimeStartSeconds % 2 === 0) {
            remainderTime.style.color = 'red';
        } else {
            remainderTime.style.color = 'black';
        }
    }
    if (remainderTimeStartSeconds == 60) {
        showAlertElement("Осталось минута до закрытия задачи, успей отправить решение.");
    }
}, 1000);


let programmingLangChooseOptions = document.querySelectorAll('#task-page__lang-choose option'),
    programmingLangChoose = document.querySelector('#task-page__lang-choose');


let codeEditor = CodeMirror(document.querySelector("#task-page__insert-code__write-code-tab__code-editor"), {
    // Объект поля с вводом кода
    value: "class test(object):\n" +
        "    ''' Строка документации '''\n" +
        "    def __init__(self, mixin=\"Hello\"):\n" +
        "        self.mixin = mixin\n" +
        "        \n" +
        "    @property\n" +
        "    def mixin_getter(self):\n" +
        "        return self.mixin\n" +
        "    \n" +
        "def maximum(a, b):\n" +
        "    if a >= b:\n" +
        "        return a\n" +
        "    return b",
    mode: 'python',
    lineNumbers: true,
    dragDrop: true,
    tabSize: 4,
    indentUnit: 4,
    matchBrackets: true,
    theme: 'default',
});


codeEditor.on('drop', function (data, e) {
    /*
        При перетаскивании файла в поле с кодом, изменяется подстветка синтаксиса
         и изменяется значение dropbox на нужный язык.
    */
    let file = e.dataTransfer.files[0];

    if ((file.name.split('.').length == 2) && (file.name.split('.')[1] in expansionToMode)) {
        let expansion = file.name.split('.')[1];

        programmingLangChooseOptions.forEach(function (option) {
            option.selected = false
        })

        programmingLangChoose.querySelector(
            `option[data-lang="${expansionToMode[expansion]}"]`
        ).selected = true;
        codeEditor.setOption("mode", expansionToMode[expansion]);
        codeEditor.setValue("");  // Очистка поля, чтобы новый был только файл открыт
        codeEditor.clearHistory();
    } else {
        e.preventDefault();
        e.stopPropagation();
        showAlertElement("Неверное расширение файла (поддерживаемые: '.py', '.c', '.cpp')");
    }
});


programmingLangChoose.onchange = function () {  // При изменении языка в dropbox, меняется подстветка синтаксиса
    let langToSelect = this.querySelector(`option[value='${this.value}']`);
    codeEditor.setOption("mode", langToSelect.dataset.lang);
};


// Кнопки для сдачи задачи
let taskPageSendFileButton = document.querySelector('.task-page__insert-code__insert-file-tab__send-button'),
    taskPageSendCodeButton = document.querySelector('.task-page__insert-code__write-code-tab__send-button'),
    taskPageLoadSolutionFileInput = document.querySelector('.task__page-load-file-input'),
    taskPageLoadSolutionFileLabel = document.querySelector('.task__page-load-file-input__label');

taskPageSendCodeButton.onclick = () => {
    let codeText = codeEditor.getValue(),
        codeLang = codeEditor.getOption('mode');

    sendTaskSolution(codeText, codeLang, 'code');
}

taskPageSendFileButton.onclick = () => {
    let file = taskPageLoadSolutionFileInput.files[0];
    if (file === undefined) {
        showAlertElement("Не загружен файл.");
        return
    }
    if (file.name.split('.').length === 2 && file.name.split('.')[1] in expansionToMode) {
        sendTaskSolution(file, expansionToMode[file.name.split('.')[1]], 'file');
    } else {
        showAlertElement("Неверное расширение файла (поддерживаемые: '.py', '.c', '.cpp')");
    }
};

taskPageLoadSolutionFileInput.onchange = function () {
    // Изменение надписи в input и выбор подходящего языка под разширение
    let file = this.files[0];
    if (file.name.split('.').length === 2 && file.name.split('.')[1] in expansionToMode) {
        let expansion = file.name.split('.')[1];

        programmingLangChooseOptions.forEach(function (option) {
            option.selected = false
        })

        programmingLangChoose.querySelector(
            `option[data-lang="${expansionToMode[expansion]}"]`
        ).selected = true;
    }
    taskPageLoadSolutionFileLabel.textContent = file.name;
};


let taskPageChangeTheme = document.querySelector('#task-page__change-code-theme__select');

taskPageChangeTheme.onchange = function () {
    let codeEditorHtmlElement = document.querySelector('.CodeMirror');
    if (this.querySelector(`option[value='${this.value}']`).dataset.themeShade === 'light') {
        codeEditorHtmlElement.style = '-webkit-box-shadow:-1px 0 0 0 #e8e8e8 inset, 0 -1px 0 0 #e8e8e8 inset, -1px -1px 0 0 #e8e8e8, -1px 0 0 0 #e8e8e8, 0 -1px 0 0 #e8e8e8;box-shadow:inset -1px 0 0 0 #e8e8e8, inset 0 -1px 0 0 #e8e8e8, -1px -1px 0 0 #e8e8e8, -1px 0 0 0 #e8e8e8, 0 -1px 0 0 #e8e8e8;'
    } else {
        codeEditorHtmlElement.style = '-webkit-box-shadow:none;box-shadow:none;';
    }
    codeEditor.setOption('theme', this.value);
};

























