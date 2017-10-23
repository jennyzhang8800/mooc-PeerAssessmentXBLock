/* Javascript for PeerAssessemntXBlock. */
function PeerAssessemntXBlock(runtime, element) {

    function reloadIndex(result) {
      
        $("#iframePage",element).attr("src",result.iframeSrc);
//        $("#content",element).text(result.content+"\n"+result.email);
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
