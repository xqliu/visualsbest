// JavaScript Document
/*获取屏幕高度*/
$(function(){
	var heights = $(document.body).height();
	$(".all_bg").css("height",heights);
});
$(function(){
	$(".fixed_time dl dd a").toggle(function(){
		$(this).css("color","#fff");
		$(this).children("span").css("background","#42BACC");	
	},function(){
		$(this).css("color","inherit");
		$(this).children("span").css("background","#fff");	
	});
	$(".fixed_time dl dd a:first-child,.fixed_time dl dd a:last-child").toggle(function(){
		$(this).css("color","#fff");
		$(this).children("span").css("background","#42BACC");	
	},function(){
		$(this).css("color","#52BECE");
		$(this).children("span").css("background","#fff");	
	});
	$(".other_time_lis span").click(function(){
		$(".all_bg,.all_neirong").css("display","block");	
	});
	$(".fixed_time_img").click(function(){
		$(".all_bg,.all_neirong").css("display","none");	
	});
});