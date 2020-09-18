$(document).ready(function () {
    let allCheckboxes = document.querySelectorAll("input[type='checkbox']");
    for (let i = 0; i < allCheckboxes.length; i++) {  // Обнуление всех чекбоксов
        allCheckboxes[i].checked = false;
    }

    let adminNotificationTableItem = document.querySelectorAll('#myTable');

    for (let i = 0; i < adminNotificationTableItem.length; i++) {
        adminNotificationTableItem[i].addEventListener('click', function () {
            let checkbox = this.querySelector('tr td .form-check-input');
            checkbox.checked = !checkbox.checked;
            if (checkbox.checked) {
                adminNotificationTableItem[i].style.background = "rgba(31,231,65,0.1)";
            } else {
                adminNotificationTableItem[i].style.background = "transparent"
            }
        })
    }


    $("#myTable tr").hide();
    $("#myInput").on("keyup", function ()
    {
        var value = $(this).val().toLowerCase();
         if (value.length == 0) {
             $.each($("#myTable tr"), function (index, value) {  // Прячет только не выделенные строки
                if (!(value.querySelector("td .form-check-input").checked)) {
                    $(value).hide();
                }
            });
         } else {
             $("#myTable tr").filter(function () {
                 if (!this.querySelector("td .form-check-input").checked)
                 {
                     $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
                 }
             });
         }
    });

    $(".notifications-filter-btn").on('click', function (event) {
        event.preventDefault();

        for (let i = 0; i < adminNotificationTableItem.length; i++) {
            let statusLabel = adminNotificationTableItem[i].querySelector('tr .status-label');

            if (statusLabel.textContent == this.dataset.statusName) {
                let checkbox = adminNotificationTableItem[i].querySelector('tr td .form-check-input');
                if (this.classList.contains("active")) {
                    checkbox.checked = false;
                    if (!$("#AllButton").hasClass("active")) {
                        $(adminNotificationTableItem[i].querySelector("tr")).hide("slow");
                    }
                    adminNotificationTableItem[i].style.background = "transparent";
                } else {
                    checkbox.checked = true;
                    $(adminNotificationTableItem[i].querySelector("tr")).show("slow");
                    adminNotificationTableItem[i].style.background = "rgba(31,231,65,0.1)";
                }
            }
        }
        this.classList.toggle("active");
    });

    var ch2 = true;
    $("#AllButton").on('click', function (event) {
        if (ch2) {
            event.preventDefault();
            $("#myTable tr").show("slow");
            $("#AllButton").addClass("active");
            $("#class10").removeClass("active");
            ch2 = !ch2;

        } else {
            event.preventDefault();

            $.each($("#myTable tr"), function (index, value) {  // Прячет только не выделенные строки
                if (!(value.querySelector("td .form-check-input").checked)) {
                    $(value).hide("slow");
                }
            });

            // $("#myTable tr").hide("slow");
            $("#AllButton").removeClass("active");
            ch2 = !ch2;
        }
    });
});
