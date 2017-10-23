# coding:utf-8
# author:zhangyanni


class Config():
    # local git repo config
    localRepoDir = '/var/www/data/os_course_exercise_library'
    localJsonFile = '%(localRepoDir)s/data/json/%(qDir)d/%(qNo)d.json'
    commitDir = 'data/json/*'
    commitEmail = 'user@example.com'
    commitName = 'www-data'
    commitText = 'debug: update %(qNo)d.json'

    # github config
    questionJsonUrl = 'https://api.github.com/repos/chyyuu/os_course_exercise_library/contents/data/json/%(qDir)d/%(qNo)d.json'
    
    # activiti API
    activitiAPIUrl = 'http://192.168.1.137:8001/workFlow/common/' 
    # log config
    logFile = '/tmp/peerAssessement_block.log'
    logFmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
