$(function ($) {
    var element = document;
    //注册markdown helper。把markdown格式转化为html
    Handlebars.registerHelper('Markdown', function (text) {
        var converter = new showdown.Converter();
        return new Handlebars.SafeString(converter.makeHtml(text));
    });

    //加载数据
    onDataLoad();
    //加载页面
    function onDataLoad() {
        //向后台请求调用接口
        parent.xblockPost({
            data: JSON.stringify({"requestType": "getStudentStatus"}),
            success: showTemplate,
            failure: handleFailure
        }, 'getStudentStatus');
    }
    //显示模板
    function showTemplate(data){
        var curStatus = eval('('+data["result"]+')');

        if(curStatus.title=="互评未开放"){
              //加载handlebars模板
            try {
                var source = $("#unStart-template").html();
                var template = Handlebars.compile(source);
                var html = template(curStatus);
                $('.peer_assessment').html(html);

            } catch (e) {
                console.info(e);
            }
        }
        else if (curStatus.title == "作业提交阶段") {
            //加载handlebars模板
            try {
                var source = $("#submit-template").html();
                var template = Handlebars.compile(source);
                var html = template(curStatus);
                $('.peer_assessment').html(html);

            } catch (e) {
                console.info(e);
            }
        }

        else if (curStatus.title == "作业互评阶段") {
            //加载handlebars模板
            try {
                var source = $("#assessment-template").html();
                var template = Handlebars.compile(source);
                var html = template(curStatus);
                $('.peer_assessment').html(html);

            } catch (e) {
                console.info(e);
            }
        }

         else if (curStatus.title == "成绩审查阶段") {
            //加载handlebars模板
            try {
                var source = $("#audit-template").html();
                var template = Handlebars.compile(source);
                var html = template(curStatus);
                $('.peer_assessment').html(html);

            } catch (e) {
                console.info(e);
            }
        }

        else if (curStatus.title == "成绩公布阶段") {
            //加载handlebars模板
            try {
                var source = $("#gradePublish-template").html();
                var template = Handlebars.compile(source);
                var html = template(curStatus);
                $('.peer_assessment').html(html);

            } catch (e) {
                console.info(e);
            }
        }
    }

    function handleFailure(XMLHttpRequest, textStatus, errorThrown) {
        makeAlart('error', 'Status: ' + XMLHttpRequest.status + ' ' + textStatus);
    }
    //转换按钮风格
    function switchStyle($el, style) {
        $el.attr('class', 'btn');
        $el.attr('disabled', false);
        if (style == 'submit') {
            $el.addClass('btn-submit');
            $el.text('再次提交');
        } else if (style == 'submiting') {
            $el.addClass('btn-submiting');
            $el.text('正在提交...');
            $el.attr('disabled', true);
        } else if (style == 'submited') {
            $el.addClass('btn-submited');
            $el.text('已提交');
            $el.attr('disabled', true);
        }
    }
    /*
     //点击“提交”按钮,绑定click事件
    $(".btn-submit").on('click', function (event) {
        answer = $('.text-input').val();
        if ($.trim(answer) == '') {
            alert('答案不能为空');
            return;
        }
        switchStyle($(event.target), 'submiting');
        //提交数据到后台
         $.ajax({
         type: 'POST',
         url: ...
         data: JSON.stringify({'answer': answer}),
         dataType: 'json',
         success: function(data) {
         switchStyle($(event.target), 'submited');
         if (data.code != 0) {
         alert('您的提交可能失败了' + JSON.stringify(data));
         } else {
         curStatus = data.result;
         onDataLoad();
         }
         }
         });
         
    });
    */

    //点击“提交”按钮,绑定click事件
    $("#btn-submit").on('click', function (event) {
        var answer = $('.text-input').val();
        if ($.trim(answer) == '') {
            alert('答案不能为空');
            return;
        }
        switchStyle($(event.target), 'submiting');  
        parent.xblockPost({
            data: JSON.stringify({"requestType": "commitPhase"}),
            success: commitDone,
            failure: handleFailure
        }, 'commitPhase');
       

    });

    function commitDone(data){

         switchStyle($(event.target), 'submited');
         if (data.success == 0) {
         alert('您的提交可能失败了' + JSON.stringify(data));
         } else {
       //  curStatus = data.result;
       //  onDataLoad();
           alert("success!");
         }
    }
});
