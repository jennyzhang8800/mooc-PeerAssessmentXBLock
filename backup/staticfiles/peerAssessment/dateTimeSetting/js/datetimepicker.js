/**
 * Created by zyni on 2017/8/22.
 */

$(function ($) {
    var element = document;
    makeAlart('info', '注意事项！设置各阶段时间，请按顺序保持时间递增');
    initDateTimePicker($('#datetimepicker1'));
    initDateTimePicker($('#datetimepicker2'));
    initDateTimePicker($('#datetimepicker3'));
    initDateTimePicker($('#datetimepicker4'));
    initDateTimePicker($('#datetimepicker5'));
    initDateTimePicker($('#datetimepicker6'));
    initDateTimePicker($('#datetimepicker7'));
    initDateTimePicker($('#datetimepicker8'));
    dataLoading();

    //保存按钮
    $('#save-btn', element).click(function (eventObjct) {
        var data = getTimeForm();
        checkTimeForm(data);

    });
    //清空按钮
    $('#clear-btn', element).click(function (eventObject) {
        clearSetting();
        $('#alart-view').empty();

    });

    function initDateTimePicker(time_object){
        time_object.datetimepicker({
        format: 'YYYY-MM-DD HH:mm:ss',
        locale: moment.locale('zh-cn')
    });
    }


    //检查时间设置是否合理
    function checkTimeForm(data) {
        $('#alart-view').empty();
        //检查是否有空的字段
        var noError = true;
        for (var key in data) {
            if (data[key] == "") {
                //$('#' + key).parent().addClass('has-error');
                makeAlart('error', '时间都不能为空！');
                noError = false;
            }
        }
        //检查时间先后顺序
        if (noError) {
            if (!(data.startTime < data.commitEndTime && data.commitEndTime < data.judgeStartTime && data.judgeStartTime < data.judgeEndTime && data.judgeEndTime < data.auditStartTime && data.auditStartTime < data.auditEndTime && data.auditEndTime < data.publishTime && data.publishTime < data.publishEndTime)) {
                makeAlart('error', '时间先后顺序有误！请重新设置');
                noError = false;
            }
        }
        //没有错误，保存
        if (noError) {
            startSaving(data);
            finishSaving(data);
        }

    }

    //加载数据
    function dataLoading() {
        //从getTimeJson接口，获得数据。
        /* parent.xblockPost({
         data: JSON.stringify(data),
         success: fillTimeForm,
         failure: handleFailure
         }, 'getTimeJson');*/

        //测试用例
          var data = {
            "startTime": "2017-08-09 08:23:43",
            "commitEndTime": "2017-08-09 08:23:46",
            "judgeStartTime": "2017-08-09 08:23:48",
            "judgeEndTime": "2017-08-09 08:23:50",
            "auditStartTime": "2017-08-09 08:23:52",
            "auditEndTime": "2017-08-09 08:23:54",
            "publishTime": "2017-08-09 08:23:56"
        };
          fillTimeForm(data);
    }

    //填充表单
    function fillTimeForm(data) {
        if (data.success = true) {
            $('#startTime').val(data.startTime);
            $('#commitEndTime').val(data.commitEndTime);
            $('#judgeStartTime').val(data.judgeStartTime);
            $('#judgeEndTime').val(data.judgeEndTime);
            $('#auditStartTime').val(data.auditStartTime);
            $('#auditEndTime').val(data.auditEndTime);
            $('#publishTime').val(data.publishTime);
            $('#publishEndTime').val(data.publishEndTime);
        }
    }

    //提交数据
    function startSaving(data) {
        $('#save-btn').text('保存中...');
        //提交数据  提交到setTimeJson 这个python handler
        /* parent.xblockPost({
         data: JSON.stringify(data),
         success: finishSaving,
         failure: handleFailure
         }, 'setTimeJson');*/

    }

    function handleFailure(XMLHttpRequest, textStatus, errorThrown) {
        makeAlart('error', 'Status: ' + XMLHttpRequest.status + ' ' + textStatus);
    }

    //清空所有的时间设置
    function clearSetting() {
        $('#startTime').val("");
        $('#commitEndTime').val("");
        $('#judgeStartTime').val("");
        $('#judgeEndTime').val("");
        $('#auditStartTime').val("");
        $('#auditEndTime').val("");
        $('#publishTime').val("");
        $('#publishEndTime').val("");
    }

    function finishSaving(data) {
        $('#save-btn').text('保存');
        /*  if(data.success == true) {
         makeAlart('success',  ' 保存成功！')
         } else {
         makeAlart('error', ' 设置失败！');
         }*/
    }

    //弹出提示
    function makeAlart(type, desc) {
        $('#alart-view').empty();
        $('#alart-view').html($('#alart-' + type + '-template').html());
        var template = $('#alart-view')
        template.find('#alart-desc').text(desc);
    }

    //获取时间设置的表单
    function getTimeForm() {
        //获取所有设置的时间
        var timeSetting = {};
        timeSetting.startTime = $('#startTime').val();
        timeSetting.commitEndTime = $('#commitEndTime').val();
        timeSetting.judgeStartTime = $('#judgeStartTime').val();
        timeSetting.judgeEndTime = $('#judgeEndTime').val();
        timeSetting.auditStartTime = $('#auditStartTime').val();
        timeSetting.auditEndTime = $('#auditEndTime').val();
        timeSetting.publishTime = $('#publishTime').val();
        timeSetting.publishEndTime = $('#publishEndTime').val();
        return timeSetting;
    }

});
