#! /bin/python
# coding:utf-8

import subprocess
from subprocess import Popen, PIPE
from conf import Config
from lib_util import Util
import codecs
import json

# gitRepo = '/Users/Heaven/git/myVim'
# p = Popen(['git', 'push'], cwd=gitRepo, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
# print p.communicate()[0]


class GitRepo():
    logger = Util.custom_logger({
        'logFile': Config.logFile,
        'logFmt': Config.logFmt,
        'logName': 'GitRepoLog'
    })

    def __init__(self, localRepoDir):
        self.localRepoDir = localRepoDir

    def execInShell(self, cmd):
        out = subprocess.check_output(cmd, shell=True)
        self.logger.debug('check_output [cmd=%s] [out=%s]' % (cmd, out))
        return out

    def checkUser(self, user):
        findEmail = self.execInShell('git config -l | grep user.email; exit 0')
        if not findEmail:
            self.execInShell('git config --global user.email "%s"' % user['email'])
        findName = self.execInShell('git config -l | grep user.name; exit 0')
        if not findName:
            self.execInShell('git config --global user.name "%s"' % user['name'])

    def pull(self):
        p = Popen(['git', 'pull'], cwd=self.localRepoDir, stdout=PIPE)
        return p.communicate()

    def status(self):
        p = Popen(['git', 'status'], cwd=self.localRepoDir, stdout=PIPE)
        return p.communicate()

    def commit(self, commit):
        p = Popen(['git', 'commit', '-m', commit], cwd=self.localRepoDir)
        return p.communicate()

    def add(self, fileRgx='--all'):
        p = Popen(['git', 'add', fileRgx], cwd=self.localRepoDir, stdout=PIPE)
        return p.communicate()

    def push(self):
        p = Popen(['git', 'push'], cwd=self.localRepoDir)
        return p.communicate()


class ExerciseRepo(GitRepo):
    def __init__(self, localRepoDir):
        self.localRepoDir = localRepoDir

    def setUser(self, user):
        self.user = user

    def setExercise(self, jsonData):
        qNo = int(jsonData['q_number'])

        # write data to file
        # filePath = '%s/data/json/%d/%d.json' % (self.localRepoDir, (qNo - 1) / 100 + 1, qNo)
        filePath = Config.localJsonFile % {
            'localRepoDir': self.localRepoDir,
            'qDir': (qNo - 1) / 100 + 1,
            'qNo': qNo,
        }
        jsonStr = json.dumps(jsonData, ensure_ascii=False, indent=4, separators=(',', ':'))
        self.saveData(filePath, jsonStr)

        # commit and push to git hub
        # self.checkUser(self.user)
        debug_add = self.add(Config.commitDir)
        debug_commit = self.commit(Config.commitText % {'qNo': qNo})
        debug_push = self.push()
        return {
            'add': debug_add,
            'commit': debug_commit,
            'push': debug_push,
        }

    def saveData(self, filePath, data):
        output = codecs.open(filePath, 'w', "utf-8")
        try:
            output.write(data)
        finally:
            output.close()

    def getMaxQNo(self):
        # update current repo
        self.pull()

        cmd_getMaxDir = 'ls %s/data/json | sort -n | tail -n 1' % self.localRepoDir
        dirNo = subprocess.check_output(cmd_getMaxDir, shell=True)
        cmd_getMaxQuestion = 'ls %s/data/json/%d | sort -n | tail -n 1' % (self.localRepoDir, int(dirNo))
        maxQJson = subprocess.check_output(cmd_getMaxQuestion, shell=True)
        return int(maxQJson.split('.')[0])

if __name__ == '__main__':
    # 这是测试程序
    repo = ExerciseRepo('/www/data/os_course_exercise_library')
    print repo.commit('commit from main')
