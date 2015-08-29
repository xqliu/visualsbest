/*banner切换*/
$(function () {
    if ($('a.preview').length) {
        var img = preloadIm();
        imagePreview(img);
    }
    $('.banner .imgs a').soChange({
        changeTime: 5000,
        thumbObj: '.banner .nums a',
        botPrev: '.banner .prev', // 按钮，上一个
        botNext: '.banner .next' // 按钮，下一个
    });
});
/*banner上面的选择*/
$(function () {
    $(".banner_top ul li").click(function () {
        $(this).children("ul").slideToggle(200);
        $(this).siblings().children("ul").slideUp(200);
    });
    $(".banner_top ul li ul").click(function (e) {
        e.stopPropagation();
    });
});
$(function () {
    $(".shooting_style li").toggle(function () {
        $(this).children("em").children("img").css("display", "block");
        $(this).siblings("li").children("em").children("img").css("display", "none");
    }, function () {
        $(this).children("em").children("img").css("display", "none");
    });
    $("ul.shooting_style li").toggle(function () {
        $(this).children("dl").stop().slideToggle(200);
        $(this).siblings("li").children("dl.one").slideUp(300);
    }, function () {
        $(this).children("dl").stop().slideUp();
    });
    $("ul.shooting_style li dl dd").click(function () {
        var span = $(this).parent().parent().children("span");
        span.text($(this).text());
        $("#" + span.attr("id") + "_id").val($(this).attr("id"));
    });
});
/*首页登录注册*/
$(function () {
    $(".denglu").click(function () {
        var $loginFixed = $(".login_fixed");
        if ($loginFixed.css('display') != 'none') {
            $loginFixed.css('display', 'none');
        } else {
            $loginFixed.show().delay(60000).hide(0);
        }
        $loginFixed.siblings(".zhuce_fixed").css("display", "none");
    });
    $(".zhuce").click(function () {
        var $zhuceFixed = $(".zhuce_fixed");
        if ($zhuceFixed.css('display') != 'none') {
            $zhuceFixed.css('display', 'none');
        } else {
            $zhuceFixed.show().delay(60000).hide(0);
        }
        $zhuceFixed.siblings(".login_fixed").css("display", "none");
    });
    $(".fixed_zhuce p a").click(function () {
        var $loginFixed = $(".login_fixed");
        if ($loginFixed.css('display') != 'none') {
            $loginFixed.show().delay(1000).hide(0);
        }
        $(".zhuce_fixed").css("display", "none");
    });
    $(".fixed_login_head a").click(function () {
        var $zhuceFixed = $(".zhuce_fixed");
        if ($zhuceFixed.css('display') != 'none') {
            $zhuceFixed.show().delay(1000).hide(0);
        }
        $(".login_fixed").css("display", "none");
    });
    $("#login_link_in_register").click(function () {
        $(".zhuce_fixed").css("display", "none");
        $(".login_fixed").show();
    });
    $("#register_link_in_login").click(function () {
        $(".login_fixed").css("display", "none");
        $(".zhuce_fixed").show();
    });

    function show_register_layer() {
        $("#fixed_zhuce_link").css('display', 'none');
        $("#fixed_zhuce_form").show();
        $(".fixed_zhuce").css('height', '450px');
        $(".zhuce_fixed").css('height', '450px');
        $(".fixed_zhuce_op").css('height', '450px');
    }

    var type_id_elem = $("#type_id");

    $("#normal_user_register_link").click(function () {
        show_register_layer();
        type_id_elem.val($("#normal_user_type_id").val());
        $("#register_button").html('注册普通用户');
    });
    $("#photographer_register_link").click(function () {
        show_register_layer();
        type_id_elem.val($("#photographer_user_type_id").val());
        $("#register_button").html('注册摄影师');
    });
    $("#login-popup-closer").click(function () {
        $(".login_fixed").css("display", "none");
    });
    $("#register-popup-closer").click(function () {
        $(".zhuce_fixed").css("display", "none");
    });
    // photo_collection_form 删除调用的代码
    $("#delete_photo_collection_link").click(function () {
        if (confirm("确定删除本作品集？")) {
            $("#photo-collection-to-delete").val($("#id").val());
            $('form[name="edit_collection_info_form"]').submit();
        }
    });
    //后台显示的提示信息显示5秒钟然后自己隐藏
    $(".flashes").delay(5000).fadeOut();
});
