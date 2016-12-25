$(function () {

    //登录输入框效果
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

    //表单验证
    $('.form_text_ipt input').bind('input propertychange', function () {
        if ($(this).val() == "") {
            $(this).css({
                'color': 'red',
            });
            $(this).parent().css({
                'border': 'solid 1px red',
            });
            // $(this).parent().next().show();
        } else {
            $(this).css({
                'color': '#333333'
            });
            $(this).parent().css({
                'border': 'solid 1px #ccc',
            });
            // $(this).parent().next().hide();
        }
    });
});

// 注册页面用户名失去焦点会调用该函数
function authentication() {
    var v = $('.form_text_ipt #username').val();
    $.get('/manager/api/auth/uname/', {'username': v}, function (msg) {
        $('.form_text_error').html(msg);
    });

}