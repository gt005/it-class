$(document).ready(function () {
    $('.content_block_table').hide();
    $('.content_block_table_future').hide();
    $('.content_toggle').click(function () {
        $('.content_block_table').slideToggle(200);
        return false;
    });
    $('.content_toggle_future').click(function () {
        $('.content_block_table_future').slideToggle(200);
        return false;
    });
});