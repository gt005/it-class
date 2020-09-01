$(document).ready(function () {
    function selection_row(odj) {
        odj.on("click", function () {
            $(this).find('input[type=checkbox]').trigger('click');
        });
    }


    $("#myTable tr").hide();
    $("#myInput").on("keyup", function () {
        var value = $(this).val().toLowerCase();
        if (value.length == 0) {
            $("#myTable tr").hide();
        } else {
            $("#myTable tr").filter(function () {
                $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
                selection_row($(this))
            });
        }
    });
    var ch2 = true;
    $("#AllButton").on('click', function (event) {
        if (ch2) {
            event.preventDefault();
            $("#myTable tr").show("slow");
            selection_row($("#myTable tr"))
            $("#AllButton").addClass("active");
            $("#class10").removeClass("active");
            ch2 = !ch2;

        } else {
            event.preventDefault();
            $("#myTable tr").hide("slow");
            $("#AllButton").removeClass("active");
            ch2 = !ch2;
        }
    });
})
;