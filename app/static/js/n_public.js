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