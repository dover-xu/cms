$(function(){

	// 百度分享
	var dataId = "";
	var picUrl = "";
	//绑定所有分享按钮所在A标签的鼠标移入事件，从而获取动态ID
	$(function () {
		$(".bdsharebuttonbox a").mouseover(function () {
			dataId = $(this).parent().attr("data-id");
			picUrl = $(this).parents(".tool-bar").siblings(".cont").find(".img-responsive").attr("src");
		});
	});
	function SetShareData(cmd, config) {
		if (dataId) {
			config.bdUrl = "http://www.hahajh.com/detail_" + dataId;
		}
		if (picUrl != null) {
			config.bdPic = "http://www.hahajh.com/" + picUrl;
		}
		return config;
	}

	function SetCount(cmd) {
		$.get('/api/a-p-t-s/', {'note_id': dataId, 'action': 'share'});
	}
	window._bd_share_config = {
		"common": {
			onBeforeClick: SetShareData,
			onAfterClick: SetCount,
			"bdSnsKey": {},
			//"bdText": "",
			"bdMini": "2",
			"bdMiniList": false,
			"bdPic": "",
			"bdStyle": "0",
			"bdSize": "16"
		},
		"share": {},
		"image": {"viewList": ["weixin", "tsina", "qzone"], "viewText": "分享到：", "viewSize": "16"},
		"selectShare": {"bdContainerClass": null, "bdSelectMiniList": ["weixin", "tsina", "qzone"]}
	};
	with (document)0[(getElementsByTagName('head')[0] || body).appendChild(createElement('script')).src = 'http://bdimg.share.baidu.com/static/api/js/share.js?v=89860593.js?cdnversion=' + ~(-new Date() / 36e5)];

	// 百度统计
	var _hmt = _hmt || [];
	(function () {
		var hm = document.createElement("script");
		hm.src = "https://hm.baidu.com/hm.js?6483835bcf6361da3ab555c65c6a541c";
		var s = document.getElementsByTagName("script")[0];
		s.parentNode.insertBefore(hm, s);
	})();

	// 悬停提示
	$(".info-name").mouseover(function () {
		$(".tips-name").fadeIn("1000");
	});
	$(".info-name").mouseout(function () {
		$(".tips-name").fadeOut("1000");
	});
	$(".info-name-s").mouseover(function () {
		$(".tips-name-s").fadeIn("1000");
	});
	$(".info-name-s").mouseout(function () {
		$(".tips-name-s").fadeOut("1000");
	});
	$(".info-signature").mouseover(function () {
		$(".tips-signature").fadeIn("1000");
	});
	$(".info-signature").mouseout(function () {
		$(".tips-signature").fadeOut("1000");
	});
	$(".info-signature-s").mouseover(function () {
		$(".tips-signature-s").fadeIn("1000");
	});
	$(".info-signature-s").mouseout(function () {
		$(".tips-signature-s").fadeOut("1000");
	});

	$(".bds_count").bind("DOMNodeInserted", function () {
		//alert('a');
	});
});
