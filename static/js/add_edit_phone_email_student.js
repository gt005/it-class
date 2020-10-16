let puplesDetailChangeEmail = document.querySelector(".puples_detail_change_email"),
    puplesDetailChangeTel = document.querySelector(".puples_detail_change_tel"),
    puplesDetailEmail = document.querySelector(".puples_detail_email"),
    puplesDetailTel = document.querySelector(".puples_detail_tel"),
    puplesDetailChangeTelEditPencil = document.querySelector(".puples_detail_change_tel__edit-pencil"),
    puplesDetailChangeEmailEditPencil = document.querySelector(".puples_detail_change_email__edit-pencil"),
    puplesDetailChangeTelCommitButton = document.querySelector(".puples_detail_change_tel__commit-btn"),
    puplesDetailChangeEmailCommitButton = document.querySelector(".puples_detail_change_email__commit-btn");

$(puplesDetailChangeEmail).hide();
$(puplesDetailChangeTel).hide();

puplesDetailChangeEmailEditPencil.onclick = function () {
    $(puplesDetailChangeEmail).fadeToggle();
}

puplesDetailChangeTelEditPencil.onclick = function () {
    $(puplesDetailChangeTel).fadeToggle();
}


let change_people_data_url = location.origin + "/statistic/pupil/{{ pk }}/";

puplesDetailChangeTelCommitButton.onclick = function () {
    let newMobileNumber = puplesDetailChangeTel.querySelector("input[type='tel']").value;

    if (newMobileNumber == "") {
        showAlertElement("Пустое поле номера телефона", false);
    } else if (!/^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{9,10}$/.test(newMobileNumber)) {
        // Если не подходит формату email
        showAlertElement("Неправильный формат телефона", false);
    } else {
        let request = getJsonResponseWithRequestData(change_people_data_url + "?edit_data=tel&tel=" + newMobileNumber);
        request.onload = function () {
            if (request.response.message == "success") {
                showAlertElement("Телефон успешно изменен!", true);
                puplesDetailTel.textContent = newMobileNumber;
                $(puplesDetailChangeTel).fadeOut();
            } else {
                showAlertElement(request.response.message, false);
            }
        }
    }

}

puplesDetailChangeEmailCommitButton.onclick = function () {
    let newEmail = puplesDetailChangeEmail.querySelector("input[type='email']").value;


    if (newEmail == "") {
        showAlertElement("Пустое поле почты", false);
    } else if (!/^([a-z0-9_-]+\.)*[a-z0-9_-]+@[a-z0-9_-]+(\.[a-z0-9_-]+)*\.[a-z]{2,6}$/.test(newEmail)) {
        // Если не подходит формату email
        showAlertElement("Неправильный формат почты", false);
    } else {
        let request = getJsonResponseWithRequestData(change_people_data_url + "?edit_data=email&email=" + newEmail);
        request.onload = function () {
            if (request.response.message == "success") {
                showAlertElement("Почта успешно изменена!", true);
                puplesDetailEmail.textContent = newEmail;
                $(puplesDetailChangeEmail).fadeOut();
            } else {
                showAlertElement(request.response.message, false);
            }
        }
    }
}