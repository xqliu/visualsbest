// JavaScript Document
function item_masonry(){ 
	$('.item img').load(function(){ 
		$('.infinite_scroll').masonry({ 
			itemSelector: '.masonry_brick',
			columnWidth:300,
			gutterWidth:15								
		});		
	});
		
	$('.infinite_scroll').masonry({ 
		itemSelector: '.masonry_brick',
		columnWidth:300,
		gutterWidth:15								
	});	
}

$(function(){

	function item_callback(){ 
		
		$('.item').mouseover(function(){
			$(this).css('box-shadow', '0 1px 5px rgba(35,25,25,0.5)');
			$('.btns',this).show();
		}).mouseout(function(){
			$(this).css('box-shadow', '0 1px 3px rgba(34,25,25,0.2)');
			$('.btns',this).hide();		 	
		});
		
		item_masonry();	

	}

	item_callback();  

	$('.item').fadeIn();

	var sp = 1
	
	$(".infinite_scroll").infinitescroll({
		navSelector  	: "#more",
		nextSelector 	: "#more a",
		itemSelector 	: ".item",
		
		loading:{
			img: "images/masonry_loading_1.gif",
			msgText: ' ',
			finishedMsg: '木有了',
			finished: function(){
				sp++;
				if(sp>=10){ //到第10页结束事件
					$("#more").remove();
					$("#infscr-loading").hide();
					$("#page").show();
					$(window).unbind('.infscr');
				}
			}	
		},errorCallback:function(){ 
			$("#page").show();
		}
		
	},function(newElements){
		var $newElems = $(newElements);
		$('.infinite_scroll').masonry('appended', $newElems, false);
		$newElems.fadeIn();
		item_callback();
		return;
	});

});