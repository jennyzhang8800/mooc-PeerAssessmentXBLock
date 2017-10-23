# coding:utf-8
# author:zhangyanni


class Config():
    # activiti API
    activitiLoginUrl = 'http://192.168.1.134:8080/api/common/loginAbutment?password=workFlow_921691866422837248&email=%(studentEmail)s&userType=%(userType)s' 
    loginAbutmentUrl = 'http://os.cs.tsinghua.edu.cn/mooc-workflow/loginAbutment?redirectUrl=/index&email=%(studentEmail)s&uuid=%(uuid)s'
    # log config
    logFile = '/tmp/peerAssessement_block.log'
    logFmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
