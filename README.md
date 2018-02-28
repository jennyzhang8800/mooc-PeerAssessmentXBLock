# mooc-PeerAssessmentXBLock
互评xblock

> 与Activiti互评系统配套，实现互评系统与Open edX平台的集成功能

## 安装指南

### 1. 安装XBlock

clone该仓库到Open edX所在机器
```
git clone https://github.com/jennyzhang8800/mooc-PeerAssessmentXBLock.git
```

进入到PeerAssessmentXBLock安装目录

```
cd mooc-PeerAssessmentXBLock/peerassessment
```

安装PeerAssessmentXBLock

```
sudo -u edxapp /edx/bin/pip.edxapp install .
```


重启Edx服务器：

```
sudo /edx/bin/supervisorctl restart edxapp:
sudo /edx/bin/supervisorctl restart edxapp_worker:
```


### 2. 把staticfiles复制到Open edX静态文件目录下

把staticfiles复制到/edx/var/edxapp/staticfiles目录下，并修改权限
```
sudo cp -r mooc-PeerAssessmentXBLock/staticfiles/* /edx/var/edxapp/staticfiles/
sudo chmod a+r -R /edx/var/edxapp/staticfiles/peerAssessment/
```

### 3. 在Open edX studio进行高级设置

studio端口为18010。例如http://cherry.cs.tsinghua.edu.cn:18010/

在“设置”-->“高级设置”中的“高级模块列表”添加该xblock的名称“peerassessment”

设置好之后，即可在课程大纲中添加该xblock(高级组件)


