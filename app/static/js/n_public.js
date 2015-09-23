// JavaScript Document
$(function () {
    $(".la").click(function () {
        $(".la_block").slideToggle(100);
        $(this).parent(".bowen").siblings(".bowen").children(".la_block").css("display", "none");
    });
    $(".bowen_xiangqing p a.all").click(function () {
        $(this).css("display", "none");
        $(this).siblings().css("display", "block");
        $(this).siblings("span").css("display", "inline");
    });
    $(".bowen_xiangqing p a.shouqi").click(function () {
        $(this).css("display", "none");
        $(this).siblings().css("display", "block");
        $(this).siblings("span").css("display", "none");
    });
});
/*预定*/
$(function () {
    $(".yuding_btn").click(function () {
        $(".all_bg,.all_neirong").css("display", "block");
        $(".").css("display", "block");
    });
    $(".fixed_time_img").click(function () {
        $(".all_bg,.all_neirong").css("display", "none");
    });
});

/*orders.html，取消、确认和拒绝拍摄请求*/
$(function () {

    function process_request(event, operation_label, operation_value) {
        event.preventDefault();
        var elemId = event.currentTarget.id;
        var request_id = elemId.substring(elemId.lastIndexOf('_') + 1, elemId.length + 1);
        if (confirm("确定" + operation_label + "本拍摄请求？")) {
            $("#operation").val(operation_value);
            $("#request_id").val(request_id);
            $('form[name="process_request"]').submit();
        }
    }

    $("button[id^='cancel_request']").click(function (e) {
        process_request(e, '取消', 'cancel');
    });
    $("button[id^='confirm_request']").click(function (e) {
        process_request(e, '确认', 'confirm');
    });
    $("button[id^='reject_request']").click(function (e) {
        process_request(e, '拒绝', 'reject');
    });
});