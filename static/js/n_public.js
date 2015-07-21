// JavaScript Document
$(function(){
	$(".la").click(function(){
		$(".la_block").slideToggle(100);
		$(this).parent(".bowen").siblings(".bowen").children(".la_block").css("display","none");
	});
	$(".bowen_xiangqing p a.all").click(function(){
		$(this).css("display","none");
		$(this).siblings().css("display","block");
		$(this).siblings("span").css("display","inline");
	});
	$(".bowen_xiangqing p a.shouqi").click(function(){
		$(this).css("display","none");
		$(this).siblings().css("display","block");
		$(this).siblings("span").css("display","none");
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
/*预定*/
$(function(){
	$(".yuding_btn").click(function(){
		$(".all_bg,.all_neirong").css("display","block");
		$(".").css("display","block");	
	});
	$(".fixed_time_img").click(function(){
		$(".all_bg,.all_neirong").css("display","none");	
	});
});