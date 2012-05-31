$(document).ready(function() {
    $(".show_comment").click(function() {
        console.log($(this).siblings());
        $(this).hide().siblings("form").show();
    })
});
