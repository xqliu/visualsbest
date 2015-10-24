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

/*orders.html，评论订单 */
$(function () {
    var overlay = $("#comment_overlay"), content = $("#comment_content");

    function show_comment_panel(e) {
        var elemId = e.currentTarget.id;
        var order_id = elemId.substring(elemId.lastIndexOf('_') + 1, elemId.length + 1);
        $("#comment_owner_id").val(order_id);
        overlay.css('display', 'block');
        content.css('display', 'block');
    }

    $("a[id^='comment_order']").click(function (e) {
        show_comment_panel(e);
    });

    $("span[id^='comment_collection']").click(function (e) {
        show_comment_panel(e);
    });
    overlay.click(function () {
        overlay.css('display', 'none');
        content.css('display', 'none');
    });
});

/*messages.html，标记 message为已读、查看message详情*/
$(function () {
    function process_msg(event, operation_label, operation_value) {
        event.preventDefault();
        var elemId = event.currentTarget.id;
        var msg_id = elemId.substring(elemId.lastIndexOf('_') + 1, elemId.length + 1);
        if (confirm("确定标记本消息为" + operation_label + "？")) {
            $("#message_operation").val(operation_value);
            $("#message_id").val(msg_id);
            $('form[name="process_message"]').submit();
        }
    }

    $("button[id^='mark_read_message']").click(function (e) {
        process_msg(e, '已读', 'read');
    });
});

/*orders.html，取消、确认和拒绝拍摄请求*/
/*orders.html，标记订单为完成和已付款*/
$(function () {

    function process_order(event, operation_label, operation_value, optional_msg) {
        event.preventDefault();
        var elemId = event.currentTarget.id;
        var order_id = elemId.substring(elemId.lastIndexOf('_') + 1, elemId.length + 1);
        if (confirm("确定标记本订单为" + operation_label + "？(" + optional_msg + ")")) {
            $("#order_operation").val(operation_value);
            $("#order_id").val(order_id);
            $('form[name="process_order"]').submit();
        }
    }

    $("a[id^='complete_order']").click(function (e) {
        process_order(e, '完成', 'complete', "请务必在摄影师提供了拍摄服务之后再进行确认");
    });
    $("a[id^='confirm_paid_order']").click(function (e) {
        process_order(e, '已付款', 'confirm_paid', "请务必在收到付款后再进行确认");
    });

    function process_request(event, operation_label, operation_value) {
        event.preventDefault();
        var elemId = event.currentTarget.id;
        var request_id = elemId.substring(elemId.lastIndexOf('_') + 1, elemId.length + 1);
        if (confirm("确定" + operation_label + "本拍摄请求？")) {
            $("#request_operation").val(operation_value);
            $("#request_id").val(request_id);
            $('form[name="process_request"]').submit();
        }
    }

    $("button[id^='cancel_request']").click(function (e) {
        process_request(e, '取消', 'cancel');
    });
    $("button[id^='confirm_request']").click(function (e) {
        process_request(e, '接受', 'confirm');
    });
    $("button[id^='reject_request']").click(function (e) {
        process_request(e, '无法接受', 'reject');
    });
    $("span[id^='g_a_style_']").unbind('click').click(function (e) {
        var elemId = e.currentTarget.id,
                style_id = elemId.substring(elemId.lastIndexOf('_') + 1, elemId.length + 1),
                elem = $("#" + elemId),
                current_class = elem.attr('class'),
                users_styles = $("#users_styles"),
                data = {
                    'unselected': {prop: true, elem_class: 'selected'},
                    'selected': {prop: false, elem_class: 'unselected'}
                };
        users_styles.find("option[value='" + style_id + "']").prop("selected", data[current_class].prop);
        elem.attr('class', data[current_class].elem_class);
    });
    $("#index_search_link").unbind('click').click(function () {
        $('form[name="search_form"]').submit();
    });
    $("a[id^='index_search_category_']").unbind('click').click(function (e) {
        var elemId = e.currentTarget.id,
                category_id = elemId.substring(elemId.lastIndexOf('_') + 1, elemId.length + 1);
        $("#index_search_category").val(category_id);
        $("#category_label").text($("#" + elemId).text());
        $(".photo_add").hide();
    });
    $("a[id^='index_search_style_']").unbind('click').click(function (e) {
        var elemId = e.currentTarget.id,
                style_id = elemId.substring(elemId.lastIndexOf('_') + 1, elemId.length + 1);
        $("#index_search_style").val(style_id);
        $("#style_label").text($("#" + elemId).text());
        $(".photo_add").hide();
    });
    $("a[id^='index_search_loc_']").unbind('click').click(function (e) {
        var elemId = e.currentTarget.id,
                loc_id = elemId.substring(elemId.lastIndexOf('_') + 1, elemId.length + 1);
        $("#index_search_loc").val(loc_id);
        $("#loc_label").text($("#" + elemId).text());
        $(".photo_add").hide();
    });
    $("a[id^='index_search_earliest_']").unbind('click').click(function (e) {
        var elemId = e.currentTarget.id,
                style_id = elemId.substring(elemId.lastIndexOf('_') + 1, elemId.length + 1);
        $("#index_search_earliest_date").val(style_id);
        $("#earliest_start_date_label").text($("#" + elemId).text());
        $(".photo_add").hide();
    });
    $("a[id^='index_search_latest_']").unbind('click').click(function (e) {
        var elemId = e.currentTarget.id,
                style_id = elemId.substring(elemId.lastIndexOf('_') + 1, elemId.length + 1);
        $("#index_search_latest_date").val(style_id);
        $("#latest_start_date_label").text($("#" + elemId).text());
        $(".photo_add").hide();
    });
});