$(function(){
		$(".praise-2").click(function(){
			var praise_img = $(this).children(".praise-img");
			//var text_box = $(".add-num-praise");
			var praise_txt = $(this).parents(".praise-1").siblings(".praise-txt");
			var num=parseInt(praise_txt.text());
			if(praise_img.attr("src") == ("images/yizan.png")){
				$(this).html("<img src='images/zan.png' class='praise-img' class='animation' />");
				praise_txt.removeClass("hover");
				//text_box.show().html("<em class='add-animation'>-1</em>");
				$(".add-animation").removeClass("hover");
				num -=1;
				praise_txt.text(num)
			}else{
				$(this).html("<img src='images/yizan.png' class='praise-img' class='animation' />");
				praise_txt.addClass("hover");
				//text_box.show().html("<em class='add-animation'>+1</em>");
				$(".add-animation").addClass("hover");
				num +=1;
				praise_txt.text(num)
			}
		});
		
		$(".tread-2").click(function(){
			var tread_img = $(this).children(".tread-img");
			//var text_box = $(".add-num-tread");
			var tread_txt = $(this).parents(".tread-1").siblings(".tread-txt");
			var num=parseInt(tread_txt.text());
			if(tread_img.attr("src") == ("images/yicai.png")){
				$(this).html("<img src='images/cai.png' class='tread-img' class='animation' />");
				tread_txt.removeClass("hover");
				//text_box.show().html("<em class='add-animation'>-1</em>");
				$(".add-animation").removeClass("hover");
				num -=1;
				tread_txt.text(num)
			}else{
				$(this).html("<img src='images/yicai.png' class='tread-img' class='animation' />");
				tread_txt.addClass("hover");
				//text_box.show().html("<em class='add-animation'>+1</em>");
				$(".add-animation").addClass("hover");
				num +=1;
				tread_txt.text(num)
			}
		});

		$("#Pagination").pagination("15");
	})

