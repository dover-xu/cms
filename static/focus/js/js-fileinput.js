/**
 * Created by xudong on 2016/12/20.
 */
//初始化fileinput
var FileInput = function () {
    var oFile = new Object();

    //初始化fileinput控件（第一次初始化）
    oFile.Initfile = function (ctrlName, uploadUrl, type_list, btn_str) {
        var control = $('#' + ctrlName);

        //初始化上传控件的样式
        control.fileinput({
            language: 'zh', //设置语言
            //uploadUrl: uploadUrl, //上传的地址
            allowedFileExtensions: type_list,//接收的文件后缀
            showUpload: false, //是否显示上传按钮
            // showRemove: false,
            showCancel: false,
            showCaption: false,//是否显示标题
            //fileActionSettings: {
            //removeIcon: '<i class="glyphicon glyphicon-trash text-danger"></i>',
            //removeClass: 'btn btn-xs btn-default',
            //removeTitle: 'Remove file',
            //uploadIcon: '<i class="glyphicon glyphicon-upload text-info"></i>',
            //uploadClass: 'btn btn-xs btn-default',
            //uploadTitle: 'Upload file',
            //indicatorNew: '<i class="glyphicon glyphicon-hand-down text-warning"></i>',
            //indicatorSuccess: '<i class="glyphicon glyphicon-ok-sign file-icon-large text-success"></i>',
            //indicatorError: '<i class="glyphicon glyphicon-exclamation-sign text-danger"></i>',
            //indicatorLoading: '<i class="glyphicon glyphicon-hand-up text-muted"></i>',
            //indicatorNewTitle: 'Not uploaded yet',
            //indicatorSuccessTitle: 'Uploaded',
            //indicatorErrorTitle: 'Upload Error',
            //indicatorLoadingTitle: 'Uploading ...'
            //},

            layoutTemplates: {
                btnBrowse: '<div tabindex="500" class="{css}"{status}>[0]</div>'.replace('[0]', btn_str)
            },
            browseClass: "btn btn-default", //按钮样式
            dropZoneEnabled: false,//是否显示拖拽区域
            minImageWidth: 80, //图片的最小宽度
            minImageHeight: 80,//图片的最小高度
            maxImageWidth: 4000,//图片的最大宽度
            maxImageHeight: 8000,//图片的最大高度
            maxFileSize: 0,//单位为kb，如果为0表示不限制文件大小
            //minFileCount: 0,
            width: '100px',
            maxFileCount: 1, //表示允许同时上传的最大文件个数
            // enctype: 'multipart/form-data',
            validateInitialCount: true,
            previewFileIcon: "<i class='glyphicon glyphicon-king'></i>",
            dropZoneTitle: '拖拽文件到这里 …',
            msgFilesTooMany: "选择上传的文件数量({n}) 超过允许的最大数值{m}！"
        });

        //导入文件上传完成之后的事件
        $("#txt_file").on("fileuploaded", function (event, data, previewId, index) {
            $("#myModal").modal("hide");
            var data = data.response.lstOrderImport;
            if (data == undefined) {
                toastr.error('文件格式类型不正确');
                return;
            }
            //1.初始化表格
            var oTable = new TableInit();
            oTable.Init(data);
            $("#div_startimport").show();
        });
    };
    return oFile;
};

function empty_check() {
    if ($('#txt_file').val() == '') {
        $('.pub-trig').css({'outline': 'none', 'box-shadow': '0 0 0 1000px #d43f3a inset'});
        $('#pic-null').stop().fadeIn(200).fadeOut(2000);
        return false;
    } else {
        $('.pub-trig').css({'outline': '1px solid #777777', 'box-shadow': '0 0 0 1000px #a94442 inset'});
        return true;
    }
}


