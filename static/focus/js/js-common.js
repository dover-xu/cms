$(function(){
	// 百度分享
	window._bd_share_config = {
		"common": {
			"bdSnsKey": {},
			"bdText": "",
			"bdMini": "2",
			"bdMiniList": false,
			"bdPic": "",
			"bdStyle": "0",
			"bdSize": "16"
		},
		"share": {},
		"image": {"viewList": ["weixin", "tsina", "qzone", "renren"], "viewText": "分享到：", "viewSize": "16"},
		"selectShare": {"bdContainerClass": null, "bdSelectMiniList": ["weixin", "tsina", "qzone", "renren"]}
	};
	with (document)0[(getElementsByTagName('head')[0] || body).appendChild(createElement('script')).src = 'http://bdimg.share.baidu.com/static/api/js/share.js?v=89860593.js?cdnversion=' + ~(-new Date() / 36e5)];

	// 登录输入框效果
	$('.form_text_ipt input').focus(function () {
		$(this).parent().css({
			'box-shadow': '0 0 3px #bbb',
		});
	});
	$('.form_text_ipt input').blur(function () {
		$(this).parent().css({
			'box-shadow': 'none',
		});
		//$(this).parent().next().hide();
	});

	// 表单验证
	$('.form_text_ipt input').bind('input propertychange', function () {
		if ($(this).val() == "") {
			$(this).css({
				'color': 'red',
			});
			$(this).parent().css({
				'border': 'solid 1px red',
			});
			//$(this).parent().next().find('span').html('helow');
			$(this).parent().next().show();
		} else {
			$(this).css({
				'color': '#ccc',
			});
			$(this).parent().css({
				'border': 'solid 1px #ccc',
			});
			$(this).parent().next().hide();
		}
	});
})

