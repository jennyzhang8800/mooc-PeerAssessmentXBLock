/* Javascript for PeerAssessemntXBlock. */
function PeerAssessemntXBlock(runtime, element) {

    function reloadIndex(result) {
      
        $("#iframePage",element).attr("src",result.iframeSrc);
         // 自动填入url指定的题号
        var urlArgs = getUrlInfo();
       
        if (urlArgs.qNo != undefined && result.userType == 'student') {
        //alert(urlArgs.qNo);
        var qNoSrc = result.indexUrl+"?view=answer&attach="+urlArgs.qNo;
//        alert(qNoSrc);
        $("#iframePage",element).attr("src",qNoSrc);
      }
    }

    var handlerUrl = runtime.handlerUrl(element, 'login');

    $(function ($) {
        /* Here's where you'd do things on page load. */
         $.ajax({
            type: "POST",
            url: handlerUrl,
            data: JSON.stringify({"login": "login"}),
            success: reloadIndex
        });

    });
}

function button_fullscreen() {
    var frame = document.getElementById("iframePage");
    if (frame.requestFullscreen) {
        frame.requestFullscreen();
    }
    else if (frame.mozRequestFullScreen) {
        frame.mozRequestFullScreen();
    }
    else if (frame.webkitRequestFullscreen) {
        frame.webkitRequestFullscreen();
    }
}

function getUrlInfo() {
        var url = window.location.search;
        var args = {};
        if (url.indexOf('?') != -1) {
            var str = url.substr(1);
            var arglist = str.split('&');
            for (var i in arglist) {
                argstr = arglist[i];
                if (argstr != null & argstr != '') {
                    var key = argstr.split('=')[0];
                    var value = argstr.split('=')[1];
                    if (args[key] == undefined) {
                        args[key] = [];
                    }
                    args[key].push(unescape(value));
                }
            }
        }
        return args;
    }

    
