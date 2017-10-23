/* Javascript for PeerAssessemntXBlock. */
var xblockPost = undefined;
function PeerAssessemntXBlock(runtime, element) {
    
    xblockPost = function(ajaxData, method) {
        ajaxData.url = runtime.handlerUrl(element, method);
        ajaxData.type = 'POST';
        $.ajax(ajaxData);
    };
    
    function settingSuccess(result) {
        alert(result.success);
    }

    var handlerUrlOnLoad = runtime.handlerUrl(element, 'onLoad');

    $(function ($) {
        /* Here's where you'd do things on page load. */
       $.ajax({
          type: "POST",
          url: handlerUrlOnLoad,
          data: JSON.stringify({"requestType":"onLoad"}),
          success: onLoading
       });

    });

    //加载页面，根据用户类型不同加载不同的页面。（教员，学生）
    function onLoading(result){
      //教师导航页面

     var TeacherIndexFrame = '<iframe src="http://cherry.cs.tsinghua.edu.cn/static/peerAssessment/index.html" frameBorder=0 id="exerciseSetting" width="100%"  height="1200px" ></iframe>'
//      var ViewIFrame = '<iframe src="http://os.cs.tsinghua.edu.cn/mooc-workflow/index?email='+result.email+'&userType='+result.userType+'" scrolling="no" frameBorder=0 id="index" width="100%"  height="1200px" ></iframe>';

      var ViewIFrame = '<iframe src="http://os.cs.tsinghua.edu.cn/mooc-workflow/loginAbutment?email='+result.email+'&userType='+result.userType+'&redirectUrl=/index" scrolling="no" frameBorder=0 id="index" width="100%"  height="1200px" ></iframe>'
      //学生展示页面frame
      var studentViewFrame = '<iframe src="http://cherry.cs.tsinghua.edu.cn/static/peerAssessment/StudentView/html/index.html" frameBorder=0 id="exerciseSetting" width="100%"  height="1200px" ></iframe>'      
      if(result["userType"]=="staff"){
         $('.peerassessment_block').html(TeacherIndexFrame);
      }
      else if(result["userType"]=="student"){
         $('.peerassessment_block').html(studentViewFrame);
      }

//     $('.peerassessment_block').html(ViewIFrame);
    }


}
