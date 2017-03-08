$(function () {

    //登录输入框效果
    $('.form_text_ipt input').focus(function () {
        $(this).parent().css({
            'box-shadow': '0 0 3px #bbb'
        });
    });
    $('.form_text_ipt #username').blur(function () {
        var object, value;
        object = $(this);
        object.parent().css({
            'box-shadow': 'none'
        });
        value = object.val();
        $.get('/manager/api/auth/uname/', {'username': value}, function (msg) {
            object.next().text(msg);
        });
    });
    $('.form_text_ipt #email').blur(function () {
        var object, value;
        object = $(this);
        object.parent().css({
            'box-shadow': 'none'
        });
        value = object.val();
    });
    $('.form_text_ipt #pw1').blur(function () {
        var object, value_pw1, value_pw2;
        object = $(this);
        object.parent().css({
            'box-shadow': 'none'
        });
        value_pw1 = object.val();
        value_pw2 = $(".form_text_ipt #pw2").val();
        $(".form_text_ipt #pw2").next().html("");
        if (value_pw2 != "" && value_pw1 != value_pw2) {
            $(".form_text_ipt #pw2").next().html("两次密码不一致");
            object.next().html("");
        } else if (value_pw1.length < 8) {
            object.next().html("至少包含8位字符");
        } else if (!isNaN(value_pw1)) {
            object.next().html("不能全为数字");
        } else {
            object.next().html("");
        }
    });
    $('.form_text_ipt #pw2').blur(function () {
        var object, value_pw1, value_pw2;
        object = $(this);
        object.parent().css({
            'box-shadow': 'none'
        });
        value_pw1 = $(".form_text_ipt #pw1").val();
        value_pw2 = object.val();
        $(".form_text_ipt #pw1").next().html("");
        if (value_pw1 != "" && value_pw1 != value_pw2) {
            object.next().html("两次密码不一致");
        } else if (value_pw2.length < 8) {
            object.next().html("至少包含8位字符");
        } else if (!isNaN(value_pw2)) {
            object.next().html("不能全为数字");
        } else {
            object.next().html("");
        }
    });

    //表单验证
    $('.form_text_ipt input').bind('input propertychange', function () {
        var value = $(this).val();
        if (value == "") {
            $(this).css({
                'color': 'red'
            });
            $(this).parent().css({
                'border': 'solid 1px red'
            });
            // $(this).parent().next().show();
        } else {
            $(this).css({
                'color': '#333333'
            });
            $(this).parent().css({
                'border': 'solid 1px #ccc'
            });
            // $(this).parent().next().hide();
        }
    });

    // 百度统计
    var _hmt = _hmt || [];
    (function () {
        var hm = document.createElement("script");
        hm.src = "https://hm.baidu.com/hm.js?6483835bcf6361da3ab555c65c6a541c";
        var s = document.getElementsByTagName("script")[0];
        s.parentNode.insertBefore(hm, s);
    })();
});
