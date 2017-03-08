/**
 * Created by Administrator on 2017/1/15.
 */
$(function () {
    //点击小图片，显示表情
    $(".bq").click(function (e) {
        $(".face").slideDown();//慢慢向下展开
        e.stopPropagation();   //阻止冒泡事件
    });

    //在桌面任意地方点击，他是关闭
    $(document).click(function () {
        $(".face").slideUp();//慢慢向上收
    });

    //点击小图标时，添加功能
    $(".face ul li").click(function () {
        var simg = $(this).find("img").clone();
        $(".message").append(simg);
    });

});
