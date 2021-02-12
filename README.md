# sonar-dingtalk
推送sonar信息到钉钉



服务端:

```
python2.7.5

pip install flask==1.1.2  requests==2.25.0
python sonar-dingtalk.py
```



客户端

```
jenkins 执行shell时添加即可
sonar有权限限制则会失败,脚本未作登录逻辑和判断


curl http://服务IP:5555/webhook?dingtalk_token=xxxxxxxxxxxxx\&project_name=$JOB_NAME\&project_key=$JOB_NAME\&sonar_server=192.168.3.183:9000\&build_number=$BUILD_NUMBER
```







