/*banner切换*/
$(function() {
	if($('a.preview').length){
		var img = preloadIm();
		imagePreview(img);
	}
	$('.banner .imgs a').soChange({
		changeTime:5000,
		thumbObj: '.banner .nums a',
		botPrev:'.banner .prev', // 按钮，上一个
		botNext:'.banner .next', // 按钮，下一个
	});
});
/*banner上面的选择*/
$(function(){
	$(".banner_top ul li").click(function(){
		$(this).children("ul").slideToggle(200);
		$(this).siblings().children("ul").slideUp(200);
	});
	$(".banner_top ul li ul").click(function(e){
		e.stopPropagation();
	});
});
$(function(){
	$(".shooting_style li").toggle(function(){
		$(this).children("em").children("img").css("display","block");
		$(this).siblings("li").children("em").children("img").css("display","none");
	},function(){
		$(this).children("em").children("img").css("display","none");
	});
	$("ul.shooting_style li").toggle(function(){
		$(this).children("dl").stop().slideToggle(200)
		$(this).siblings("li").children("dl.one").slideUp(300);
	},function(){
		$(this).children("dl").stop().slideUp();
	});
});
/*首页登录注册*/
$(function(){
	$(".denglu").click(function(){
		if ($(".login_fixed").css('display') != 'none') {
			$(".login_fixed").css('display', 'none');
		} else {
		    $(".login_fixed").show().delay(10000).hide(0);
	    }
		$(".login_fixed").siblings(".zhuce_fixed").css("display","none");
	});
	$(".zhuce").click(function(){
		if ($(".zhuce_fixed").css('display') != 'none') {
			$(".zhuce_fixed").css('display', 'none');
		} else {
			$(".zhuce_fixed").show().delay(10000).hide(0);
		}
		$(".zhuce_fixed").siblings(".login_fixed").css("display","none");
	});
	$(".fixed_zhuce p a").click(function(){
		if ($(".login_fixed").css('display') != 'none')	{
			$(".login_fixed").show().delay(1000).hide(0);
    	}
		$(".zhuce_fixed").css("display","none");
	});
	$(".fixed_login_head a").click(function(){
		if ($(".zhuce_fixed").css('display') != 'none')	{
			$(".zhuce_fixed").show().delay(1000).hide(0);
		}
		$(".login_fixed").css("display","none");
	});
	$("#login_link_in_register").click(function(){
		$(".zhuce_fixed").css("display","none");
		$(".login_fixed").show();
	});
	$("#register_link_in_login").click(function(){
		$(".login_fixed").css("display","none");
		$(".zhuce_fixed").show();
	});

});
