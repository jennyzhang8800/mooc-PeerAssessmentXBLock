"""TO-DO: Write a description of what this XBlock is."""
# coding:utf-8
# author:zhangyanni
import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, Integer
from xblock.fragment import Fragment
from conf import Config
from lib_util import Util
import urllib2
import json
import base64
class PeerAssessemntXBlock(XBlock):
    """
    TO-DO: document what your XBlock does.
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.

    # TO-DO: delete count, and define your own fields.
    count = Integer(
        default=0, scope=Scope.user_state,
        help="A simple counter, to show something happening",
    )

    logger = Util.custom_logger({
        'logFile': Config.logFile,
        'logFmt': Config.logFmt,
        'logName': 'PeerAssessmentXBlockLog'
    })

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the PeerAssessemntXBlock, shown to students
        when viewing courses.
        """
        html = self.resource_string("static/html/peerassessment.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/peerassessment.css"))
        frag.add_javascript(self.resource_string("static/js/src/peerassessment.js"))
        frag.initialize_js('PeerAssessemntXBlock')
        return frag

    # TO-DO: change this handler to perform your own actions.  You may need more
    # than one handler, or you may not need any handlers at all.
    @XBlock.json_handler
    def login(self, data, suffix=''):
        """
        An example handler, which increments the data.
        """
        # Just to show data coming in...
        student = self.runtime.get_real_user(self.runtime.anonymous_student_id)
        studentEmail = student.email
        studentType = "staff" if student.is_staff else "student"
        activitiLoginUrl = Config.activitiLoginUrl % {
            'studentEmail': studentEmail,
            'userType': studentType,
        } 
        #url="https://api.github.com/repos/chyyuu/os_course_exercise_library/contents/data/json/16/1502.json"
        try:
            res_data = urllib2.urlopen(activitiLoginUrl)
            res = res_data.read()
            res = json.loads(res)
            
            uuid = res["data"]["uuid"]
           
            loginAbutmentUrl = Config.loginAbutmentUrl % {
                'studentEmail':studentEmail,
                'uuid':uuid,
            }
            return {"iframeSrc": loginAbutmentUrl,"content":activitiLoginUrl,"email":loginAbutmentUrl}
          
        except Exception as e:
            return {"iframeSrc":"","content":"","email":studentEmail,"error":str(e)}
    
    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("PeerAssessemntXBlock",
             """<peerassessment/>
             """),
            ("Multiple PeerAssessemntXBlock",
             """<vertical_demo>
                <peerassessment/>
                <peerassessment/>
                <peerassessment/>
                </vertical_demo>
             """),
        ]
