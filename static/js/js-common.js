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
})

