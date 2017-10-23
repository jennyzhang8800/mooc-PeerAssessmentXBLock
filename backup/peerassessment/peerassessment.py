# coding:utf-8
# author:zhangyanni
import pkg_resources
from gitRepo import ExerciseRepo
from conf import Config
from lib_util import Util
from xblock.core import XBlock
from xblock.fields import Scope, Integer
from xblock.fragment import Fragment
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

    # 当前block保存的题题号
    qNo = Integer(default=0, scope=Scope.content)

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
        frag.add_javascript_url('//cdn.bootcss.com/handlebars.js/4.0.5/handlebars.min.js')
        frag.add_javascript_url('//cdn.bootcss.com/showdown/1.3.0/showdown.min.js')
        frag.add_javascript(self.resource_string("static/js/src/peerassessment.js"))
        frag.initialize_js('PeerAssessemntXBlock')
        return frag

    # TO-DO: change this handler to perform your own actions.  You may need more
    # than one handler, or you may not need any handlers at all.

    @XBlock.json_handler
    def getQuestionJson(self, data, suffix=''):
        q_number = int(data['q_number'])
        url = Config.questionJsonUrl % {
            'qDir': ((q_number - 1) / 100) + 1,
            'qNo': q_number,
        }
        try:
            #req = urllib2.Request(url)
            res_data = urllib2.urlopen(url)
            res = res_data.read()
            res = json.loads(res)
            if 'content' in res:
                content = json.loads(base64.b64decode(res['content']))
                self.logger.info('getQuestionJson [qNo=%d] [url=%s]' % (q_number, url))
                return {'code': 0, 'desc': 'ok', 'res': content}
            elif res['message'] == 'Not Found':
                self.logger.info('ERROR getQuestionJson [qNo=%d] [msg=%s] [url=%s]' % (q_number, res['message'], url))
                return {'code': 1, 'type': 'error', 'desc': u'题号为%d的题目不存在' % q_number}
            else:
                self.logger.info('ERROR getQuestionJson [qNo=%d] [msg=%s] [url=%s]' % (q_number, res['message'], url))
                return {'code': 1, 'error': 'error', 'dese': 'Error occurs when loading %d.json message: %s' % (q_number, res['message'])}
        except Exception as e:
            self.logger.exception('ERROR getQuestionJson [qNo=%d] [desc=%s] [url=%s]' % (q_number, str(e), url))
            return {
                'code': 1,
                'type': 'error',
                'desc': str(e),
            }

    @XBlock.json_handler
    def setQuestionJson(self, data, suffix=''):
        try:
            repo = ExerciseRepo(Config.localRepoDir)
            repo.setUser({'email': Config.commitEmail, 'name': Config.commitName})
            # 简单检查题目是否合理
            lenOfAnswer = len(data['answer'].strip())
            questionType = data['type']
            if lenOfAnswer == 0:
                return {'code': 2, 'type': 'warning', 'desc': '答案不能为空'}
            if questionType == 'single_answer' and lenOfAnswer != 1:
                return {'code': 2, 'type': 'warning', 'desc': '单选题的答案个数仅有一个'}

            data['status'] = 'ok'

            if not data['q_number']:
                data['q_number'] = repo.getMaxQNo() + 1
            repo.setExercise(data)
            self.logger.info('setQuestionJson [qNo=%d] [%s]' % (data['q_number'], json.dumps(data)))
            return {'code': 0, 'q_number': data['q_number']}
        except Exception as e:
            self.logger.exception('ERROR setQuestionJson [qNo=%d] [desc=%s] [%s]' % (data['q_number'], str(e), json.dumps(data)))
            return {'code': 1, 'type': 'error', 'desc': '发生错误, %s' % str(e)}
    
    @XBlock.json_handler
    def onLoad(self,data,suffix=''):
        """
        页面加载时，判断用户类型。
        """
        student = self.runtime.get_real_user(self.runtime.anonymous_student_id)
        studentEmail = student.email
        if(student.is_staff):
            return {"userType":"staff","email":studentEmail}
        else:
            return {"userType":"student","email":studentEmail}

    @XBlock.json_handler
    def questionInitLoad(self,data,suffix=''):
        """
        题目布置页面，初始加载，检查是否己经布置过题目
        """
        if(self.qNo==0):
            return {"qNo":0,"type":"info","desc":"尙未布置题目"}
        else:
            qDir=((self.qNo - 1) / 100) + 1
            q_number=self.qNo
            try:
                APIUrl = Config.activitiAPIUrl+ "getQAContent?qDir=%(qDir)s,qNo=%(qNo)s" % {'qDir':qDir,'qNo':self.qNo}
                res_data = urllib2.urlopen(APIUrl)
                res = res_data.read()
                res = json.loads(res)
                if 'content' in res:
                    content = json.loads(base64.b64decode(res['content']))
                    self.logger.info('getQuestionJson [qNo=%d] [url=%s]' % (q_number, APIUrl))
                    return {'code': 0, 'desc': 'ok', 'res': content}
                elif res['message'] == 'Not Found':
                    self.logger.info('ERROR getQuestionJson [qNo=%d] [msg=%s] [url=%s]' % (q_number, res['message'], APIUrl))
                    return {'code': 1, 'type': 'error', 'desc': u'题号为%d的题目不存在' % q_number}
                else:
                    self.logger.info('ERROR getQuestionJson [qNo=%d] [msg=%s] [url=%s]' % (q_number, res['message'], APIUrl))
                    return {'code': 1, 'error': 'error', 'dese': 'Error occurs when loading %d.json message: %s' % (q_number, res['message'])}
            except Exception as e:
                self.logger.exception('ERROR questionInitLoad [desc=%s] [%s]' % ( str(e), json.dumps(data)))
                return {'success': 0, 'type': 'error', 'desc': '发生错误, %s' % str(e)}

    @XBlock.json_handler
    def getStudentStatus(self,data,suffix=''):
        """
          获得学生状态，及要显示的数据
        """
        curStatus = {"title": "作业提交阶段","question": "下面是SFS的磁盘索引节点数据结构定义。\n```\nstruct sfs_disk_inode {\n    uint32_t size;\n    uint16_t type;\n    uint16_t nlinks;\n    uint32_t blocks;\n    uint32_t direct[SFS_NDIRECT];\n    uint32_t indirect;\n};\n```\n假定ucore 里 SFS_NDIRECT的取值是16，而磁盘上数据块大小为1KB。请计算这时ucore支持的最大文件大小。请给出计算过程。（这样可给步骤分）"}
        student = self.runtime.get_real_user(self.runtime.anonymous_student_id)
         
        try:
            #APIUrl = Config.activitiAPIUrl+ "getStudentStatus?email=%(email)s" % {'email':student.email}
            url='http://192.168.1.137:8000/workFlow/common/getQAContent?qDir=16&qNo=1570'
            res_data = urllib2.urlopen(url)
            res = res_data.read()
            res = json.loads(res)
            return {"success":1,"result":json.dumps(res)}
            #return {"success":1,"result":json.dumps(curStatus)}
        except Exception as e:
            self.logger.exception('ERROR getStudentStatus [desc=%s] [%s]' % ( str(e), json.dumps(data)))
            return {'success': 0, 'type': 'error', 'desc': '发生错误, %s' % str(e)}

    @XBlock.json_handler
    def getTimeJson(self,data,suffix=''):
        """
        Get Time Setting From API
        """   
        try:  
            data["courseName"]="os_course"
            data["courseCode"]="course-v1:Tsinghua+OS101+2016_T1"
            #url = Config.activitiAPIUrl+ "getScheduleTime?schedule=%(schedule)s" % {'schedule':json.dumps(data)}
            #url='http://192.168.1.137:8000/workFlow/common/getQAContent?qDir=16&qNo=1570'
            url = 'http://192.168.1.137:8000/workFlow/common/selectScheduleTime?courseCode=%(courseCode)s' % {'courseCode':data["courseCode"]}
            res_data = urllib2.urlopen(url)
            res = res_data.read()
            res = json.loads(res)
            return {"result": json.dumps(res),"url":url}
            #return {"hasTimeSetting":0,"result":url} 
        except Exception as e:
            self.logger.exception('ERROR getTimeJson [desc=%s] [%s]' % ( str(e), json.dumps(data)))
            return {'success': 0, 'type': 'error', 'desc': '发生错误, %s' % str(e)}
    @XBlock.json_handler
    def setTimeJson(self,data,suffix=''):
        """
        Set Time 
        """
        try:
            data["courseName"]="os_course"
            data["courseCode"]="course-v1:Tsinghua+OS101+2016_T1"
            url = "http://192.168.1.137:8000/workFlow/common/insertScheduleTime?schedule=%(schedule)s" % {'schedule':json.dumps(data)}      
            res_data = urllib2.urlopen(url)
            res = res_data.read()
            res = json.loads(res)
            return {"success": json.dumps(res)}
            #return {"success":1,"result":url} 
        except Exception as e:
            self.logger.exception('ERROR setTimeJson [desc=%s] [%s]' % ( str(e), json.dumps(data)))
            return {'success': 0, 'url':url,'type': 'error', 'desc': '发生错误, %s' % str(e)} 
    @XBlock.json_handler
    def commitPhase(self,data,suffix=''):
        """
          commit excercise
        """
        student = self.runtime.get_real_user(self.runtime.anonymous_student_id)
        data["email"]=student.email
        try:
            url = Config.activitiAPIUrl + "commitExercise?..."
            # res_data = urllib2.urlopen(url)
            # res = res_data.read()
            # res = json.loads(res)
            # return {"success":1,"result":res}
            return {"success":1,"result":data}
        except Exception as e:
            self.logger.exception('ERROR setTimeJson [desc=%s] [%s]' % ( str(e), json.dumps(data)))
            return {'success': 0, 'type': 'error', 'desc': '发生错误, %s' % str(e)}

    @XBlock.json_handler
    def teacher_settings(self, data, suffix=''):
        """
        An example handler, which increments the data.
        """
        # Just to show data coming in...
        data["courseName"]="os_course"
        data["courseCode"] ="course-v1:Tsinghua+OS101+2016_T1"

        url = Config.activitiAPIUrl+ "insertScheduleTime?schedule=%(schedule)s" % {'schedule':json.dumps(data)}
        res_data = urllib2.urlopen(url)
        res = res_data.read()
        res = json.loads(res)
        return {"success": json.dumps(res)}

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
