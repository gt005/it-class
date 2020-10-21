function showAlertElement(message, success=false) {
    let alertElement = `<div class="system-message alert alert-danger alert-dismissible fade show" id="alert-msg" role="alert"><span class="alert-msg-text">${message}</span> <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button> </div>`;

    if (success === true)
    {
        alertElement = `<div class="system-message alert alert-success alert-dismissible fade show" id="alert-msg" role="alert"><span class="alert-msg-text">${message}</span> <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button> </div>`;
    }

    document.querySelector(".messages-container").innerHTML += alertElement;

    $(".system-message").delay(10000).fadeOut();
}

function convertSecondsToHoursAndMinutes(seconds) {
    if (seconds < 0) {
        seconds = 0;
    }
    let resultTime = ``;
    if (Math.trunc(seconds / 3600) !== 0) {
        resultTime += `${Math.trunc(seconds / 3600)} ч. `
    }
    if (Math.trunc(seconds % 3600 / 60) !== 0) {
        resultTime += `${Math.trunc(seconds % 3600 / 60)} мин. `
    }
    if (Math.trunc(seconds % 60) !== 0) {
        resultTime += `${seconds % 60} сек`
    }

    console.log(
        resultTime
    )
    return resultTime
}

// Страница с задачей
let remainderTime = document.querySelector("#task-page__time-remainder__time"),
    remainderTimeStartSeconds = remainderTime.textContent;

remainderTime.textContent = convertSecondsToHoursAndMinutes(remainderTimeStartSeconds);

let remainderTimeInterval = setInterval(function () {
    remainderTimeStartSeconds--;
    remainderTime.textContent = convertSecondsToHoursAndMinutes(remainderTimeStartSeconds);
    if (remainderTimeStartSeconds <= 0) {
    //    Удалять страницу и отправлять результат
        remainderTime.textContent = "Время закончилось";
        remainderTime.style.color = 'red';
        showAlertElement("Время вышло!");
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
