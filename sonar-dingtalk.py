#!/usr/bin python
# -*- encoding: utf-8 -*-
# 
from flask import Flask
from flask import request, jsonify, abort
import json
import subprocess
import requests

import sys
reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':

        dingtalk_url="https://oapi.dingtalk.com/robot/send?access_token="
        dingtalk_token = request.args.get("dingtalk_token")
        dingtalk_webhook=dingtalk_url+dingtalk_token

        project_name=request.args.get("project_name")
        project_key=request.args.get("project_key")
        sonar_server=request.args.get("sonar_server")
        build_number=request.args.get("build_number")


        bug = '0'
        leak = '0'
        code_smell = '0'
        coverage = '0'
        density = '0'
        status = ''
        statusStr = ''
        picUrl=''

        sonar_Url ='http://'+str(sonar_server)+'/api/measures/search?projectKeys='+str(project_key)+'&metricKeys=alert_status%2Cbugs%2Creliability_rating%2Cvulnerabilities%2Csecurity_rating%2Ccode_smells%2Csqale_rating%2Cduplicated_lines_density%2Ccoverage%2Cncloc%2Cncloc_language_distribution'
        resopnse = requests.get(sonar_Url).text
        # 转换成josn
        result = json.loads(resopnse)


        # 解析sonar json结果
        for item in result['measures']:
            if item['metric']=="bugs":
                bug = item['value']
            elif item['metric']=="vulnerabilities":
                leak = item['value']
            elif item['metric']=='code_smells':
                code_smell = item['value']
            elif item['metric']=='coverage':
                coverage = item['value']
            elif item['metric']=='duplicated_lines_density':
                density = item['value']
            elif item['metric']=='alert_status':
                status = item['value']
            else:
                pass

        # 判断新代码质量阀状态
        if status == 'ERROR':
            # 错误图片
            picUrl = 'http://www.iconsdb.com/icons/preview/soylent-red/x-mark-3-xxl.png'
            statusStr = '失败'
        elif status == 'OK':
            statusStr = '通过'
            # 正确图片
            picUrl = 'http://icons.iconarchive.com/icons/paomedia/small-n-flat/1024/sign-check-icon.png'

        # 消息内容。如果太长只会部分展示
        code_reslut=  "Bug数:" + bug + "个，" + \
                      "漏洞数:" + leak + "个，" + \
                      "可能存在问题代码:"+ str(code_smell) + "行，" + \
                      "覆盖率:" + str(coverage) + "%，" + \
                      "重复率:" + str(density) + "%"


        pagrem = {
            "msgtype": "link",
            "link": {
                'title':'sonar scan ' + project_name +'#'+build_number + ' 点击查看',
                "text": code_reslut,
                'picUrl': picUrl,
                'messageUrl':'http://'+sonar_server+'/dashboard?id='+ project_name
            }
        }

        headers = {
            'Content-Type': 'application/json'
        }

        # 发送钉钉消息
        requests.post(dingtalk_webhook, data=json.dumps(pagrem), headers=headers)


        return jsonify({'status': 'success'}), 200

    else:
        abort(400)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5555')
