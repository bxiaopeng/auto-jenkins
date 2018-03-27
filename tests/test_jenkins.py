#!/usr/bin/python
# -*- coding:utf-8 -*- 
# ---------------------------------------------------------------------------
#  Name:           test_jenkins.py
#  Description:    添加描述信息
#
#  Created:        2017/11/16 下午4:21
#  Author:         bixiaopeng
#  Email:          wirelessqa@163.com
#  OS:             Mac OS X
#  Python Version: 3.6.4
# ---------------------------------------------------------------------------
import pprint
import time
import ujson

import pytest
import requests

import autojenkins


@pytest.mark.skip
def test_jenkins():
    # 定义远程的jenkins master server的url，以及port
    jenkins_server_url = 'http://192.168.150.191:8080/jenkins/'

    # 定义用户的User Id 和 API Token
    username = 'admin'
    password = 'admin'

    # 实例化jenkins对象，连接远程的jenkins master server
    server = jenkins.Jenkins(jenkins_server_url, username=username, password=password)

    # 获取一个 jenkins 下的所有 JOB 的信息
    all_jobs = server.get_all_jobs()

    for job in all_jobs:
        name = job.get('name')
        url = job.get("url")
        color = job.get('color')  # red/blue

        print("name: {}".format(name))
        print("url: {}".format(url))
        print("color: {}".format(color))

    job_name = 'api-test'

    print("=============== job info  ===============")

    # # 任务的详细信息
    print(ujson.dumps(server.get_job_info(job_name)))  # 一个 json

    print("描述 description： {}".format(server.get_job_info(job_name).get("description")))
    print("颜色 color： {}".format(server.get_job_info(job_name).get("color")))
    print("显示全名 fullDisplayName： {}".format(server.get_job_info(job_name).get("fullDisplayName")))
    print("最近一次构建 lastBuild： {}".format(server.get_job_info(job_name).get("lastBuild")))

    # # 最后一次的构建号 server.get_job_info(job_name)['lastBuild']['number']

    print("最近一次稳定构建 lastStableBuild： {}".format(server.get_job_info(job_name).get("lastStableBuild")))
    print("最近一次失败构建 lastFailedBuild： {}".format(server.get_job_info(job_name).get("lastFailedBuild")))
    print("下一个构建号 nextBuildNumber： {}".format(server.get_job_info(job_name).get("nextBuildNumber")))
    print("最近一次不成功的构建 lastUnsuccessfulBuild： {}".format(server.get_job_info(job_name).get("lastUnsuccessfulBuild")))
    print("最近一次完整构建 lastCompletedBuild： {}".format(server.get_job_info(job_name).get("lastCompletedBuild")))
    print("最近一次成功构建 lastSuccessfulBuild： {}".format(server.get_job_info(job_name).get("lastSuccessfulBuild")))

    print("inQueue： {}".format(server.get_job_info(job_name).get("inQueue")))
    print("buildable： {}".format(server.get_job_info(job_name).get("buildable")))
    print("concurrentBuild： {}".format(server.get_job_info(job_name).get("concurrentBuild")))
    print("queueItem： {}".format(server.get_job_info(job_name).get("queueItem")))
    print("健康报告 healthReport： {}".format(server.get_job_info(job_name).get("healthReport")))
    print("actions： {}".format(server.get_job_info(job_name).get("actions")))
    print("scm： {}".format(server.get_job_info(job_name).get("scm")))

    print("")
    print("========== property: ")

    property = server.get_job_info(job_name).get('property')

    # 遍历属性
    for p in property:
        # 遍历参数
        para_defins = p.get('parameterDefinitions')

        if para_defins:
            for pd in para_defins:
                print("description: {}".format(pd.get('description')))
                print("defaultParameterValue: {}".format(pd.get("defaultParameterValue")))
                print("choices： {}".format(pd.get('choices')))
                print("type: {}".format(pd.get('type')))
                print("name: {}".format(pd.get('name')))

            #
            # # String 参数化构建job名为k8s-new的job, 参数param_dict为字典形式
            # param_dict = {"module": "all", "env": "test"}
            #
            # # 构建任务
            # # server.build_job(job_name, parameter_defines=param_dict)
            #

            # # 获取job名为job_name的job的某次构建的执行结果状态
            # print server.get_build_info(job_name, build_number)['result']  # FAILURE

            # print server.get_job_config(job_name)  # XML 信息

            # print server.get_build_console_output(job_name,build_number)  # 输出日志

    # 最后一次的构建号
    build_number = server.get_job_info(job_name)['lastBuild']['number']
    # 获取构建信息
    print(ujson.dumps(server.get_build_info(job_name, build_number)))

    print("正在构建： {}".format(server.get_build_info(job_name, build_number).get("building")))
    print("result： {}".format(server.get_build_info(job_name, build_number).get("result")))
    print("queueId： {}".format(server.get_build_info(job_name, build_number).get("queueId")))
    print("displayName： {}".format(server.get_build_info(job_name, build_number).get("displayName")))
    print("fullDisplayName： {}".format(server.get_build_info(job_name, build_number).get("fullDisplayName")))
    print("timestamp： {}".format(server.get_build_info(job_name, build_number).get("timestamp")))
    print("duration： {}".format(server.get_build_info(job_name, build_number).get("duration")))
    print("estimatedDuration： {}".format(server.get_build_info(job_name, build_number).get("estimatedDuration")))
    print("actions： {}".format(server.get_build_info(job_name, build_number).get("actions")))
    print("url： {}".format(server.get_build_info(job_name, build_number).get("url")))
    print("allure url： {}".format(server.get_build_info(job_name, build_number).get("url") + "allure"))

    allure_data_url = server.get_build_info(job_name, build_number).get("url") + "allure/data/widgets.json"
    print("allure data(json)： {}".format(allure_data_url))

    # allure 报告
    allure_data_json = requests.get(allure_data_url, auth=(username, password)).json()


@pytest.mark.skip
def test_requests_jenkins_url():
    url = 'http://192.168.150.191:8080/jenkins/job/api-test/320/allure/data/widgets.json'
    auth = ('admin', 'admin')
    headers = {"Content-Type": "application/xml"}
    allure_data_json = requests.get(url, auth=auth).json()

    print(allure_data_json)
    print(type(allure_data_json))
    print(allure_data_json["summary"]["statistic"])
    items = allure_data_json["behaviors"]["items"]

    for i in items:
        print(i.get("name"))
        print(i)

    statistic = allure_data_json["summary"]["statistic"]

    print(statistic)

    failed = statistic.get('failed')
    broken = statistic.get('broken')
    skipped = statistic.get('skipped')
    passed = statistic.get('passed')
    unknown = statistic.get('unknown')
    total = statistic.get('total')

    print(passed)
    print(total)

    print('%d%%' % (round((skipped + passed) / float(total), 2) * 100))

    print('%d' % (round((skipped + passed) / float(total), 2) * 100))
    print(type('%d' % round((skipped + passed) / float(total), 2) * 100))
    aaa = int('%d' % round((skipped + passed) / float(total), 2) * 100)
    print(type(aaa))

    # time_duration = allure_data_json["summary"]["time"]['duration']
    #
    # print time_duration
    #
    # m, s = divmod(time_duration/1000, 60)
    # h, m = divmod(m, 60)
    #
    # print "%d:%02d:%02d" % (h, m, s)


@pytest.mark.skip
def test_lastbuild_time():
    import arrow
    # 定义远程的jenkins master server的url，以及port
    jenkins_server_url = 'http://192.168.150.191:8080/jenkins/'

    # 定义用户的User Id 和 API Token
    username = 'admin'
    password = 'admin'

    # 实例化jenkins对象，连接远程的jenkins master server
    server = jenkins.Jenkins(jenkins_server_url, username=username, password=password)
    job_name = 'api-test-taxIt'
    # 最后一次的构建号
    build_number = server.get_job_info(job_name)['lastBuild']['number']
    timestap = server.get_build_info(job_name, build_number).get("timestamp")

    print(arrow.get(timestap / 1000).to('local').format('YYYY-MM-DD HH:mm:ss'))
    print(arrow.get(timestap / 1000).to('local').humanize(locale="zh"))


@pytest.mark.skip
def test_request_json():
    username = 'admin'
    password = 'admin'
    # server = jenkins.Jenkins("http://10.199.134.13:8080/jenkins/", username=username, password=password)

    # data_json = requests.get('http://10.199.134.13:8080/jenkins/job/api-statictis/ws/apiresult.json',
    #                          auth=(username, password)).json()

    data_json = requests.get('http://192.168.150.191:8080/jenkins/job/api-test-finance/100/allure/widgets/summary.json',
                             auth=(username, password)).json()

    print(data_json)
    # print(type(data_json))
    #
    # print(data_json.get('api-test-boss'))


@pytest.mark.skip
def test_jenkins_usage():
    server = jenkins.Jenkins(url="http://192.168.150.191:8080/jenkins/", username="admin", password="admin")

    # 获取用户账户信息
    whoami = server.get_whoami()

    # 获取用户名
    assert whoami['fullName'] == "admin"

    # 新建一个任务
    server.create_job('my-jenkins-example', jenkins.EMPTY_CONFIG_XML)

    # 断言某个任务已存在
    server.assert_job_exists('my-jenkins-example')

    # 获取所有任务
    jobs = server.get_jobs()
    # 返回的结果是一个列表
    assert isinstance(jobs, list)
    # 列表中是N个字典
    assert isinstance(jobs[0], dict)
    # 任务的数量
    assert len(jobs) == server.jobs_count()

    # 获取已存在的任务的配置
    my_job = server.get_job_config('my-jenkins-example')
    print(my_job)  # 打印 XML 配置

    # 构建一个任务
    server.build_job('my-jenkins-example')
    # 禁用一个任务
    server.disable_job('my-jenkins-example')
    # 复制一个任务
    server.copy_job('my-jenkins-example', 'my-jenkins-example-copy')
    # 启用一个任务
    server.enable_job('my-jenkins-example-copy')
    # 重新配置任务
    server.reconfig_job('my-jenkins-example-copy', jenkins.RECONFIG_XML)
    # 删除任务
    server.delete_job('my-jenkins-example')
    server.delete_job('my-jenkins-example-copy')


TEST_JENKINS_CONFIG_XML = '''<?xml version='1.0' encoding='UTF-8'?>
<project>
  <actions/>
  <description></description>
  <keepDependencies>false</keepDependencies>
  <properties>
    <hudson.model.ParametersDefinitionProperty>
      <parameterDefinitions>
        <hudson.model.StringParameterDefinition>
          <name>param_str</name>
          <description></description>
          <defaultValue></defaultValue>
        </hudson.model.StringParameterDefinition>
        <hudson.model.BooleanParameterDefinition>
          <name>param_boolean</name>
          <description></description>
          <defaultValue>false</defaultValue>
        </hudson.model.BooleanParameterDefinition>
        <hudson.model.ChoiceParameterDefinition>
          <name>param_choice</name>
          <description></description>
          <choices class="java.util.Arrays$ArrayList">
            <a class="string-array">
              <string>a</string>
              <string>b</string>
              <string>c</string>
            </a>
          </choices>
        </hudson.model.ChoiceParameterDefinition>
      </parameterDefinitions>
    </hudson.model.ParametersDefinitionProperty>
  </properties>
  <scm class="hudson.scm.NullSCM"/>
  <canRoam>true</canRoam>
  <disabled>false</disabled>
  <blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>
  <blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
  <triggers/>
  <concurrentBuild>false</concurrentBuild>
  <builders>
    <hudson.tasks.Shell>
      <command>echo ${param_str}
echo ${param_boolean}
echo ${param_choice}</command>
    </hudson.tasks.Shell>
  </builders>
  <publishers/>
  <buildWrappers/>
</project>
'''


@pytest.mark.skip  # pass,但不想每次都新建和删除
def test_jenkins_complex():
    server = jenkins.Jenkins(url="http://192.168.150.191:8080/jenkins/", username="admin", password="admin")
    server.create_job('test-jenkins', TEST_JENKINS_CONFIG_XML)

    # 构建带参数 test-jenkins 任务，接受不同类型的参数
    server.build_job('test-jenkins',
                     {
                         'param_str': 'my str param',
                         'param_boolean': False,
                         'param_choice': "c"
                     })

    time.sleep(10)  # 等任务构建完，请自行调整时间
    # 断言任务已存在
    server.assert_job_exists("test-jenkins")

    # 最后的构建号
    try:
        last_build_number = server.get_job_info('test-jenkins')['lastCompletedBuild']['number']
        print(last_build_number)  # >>> 2
        # 最后的构建信息
        build_info = server.get_build_info('test-jenkins', last_build_number)
        print(build_info)
    except:
        pass

    # 删除任务
    server.delete_job("test-jenkins")

    # 从指定的视图获取所有任务列表
    jobs = server.get_jobs(view_name='All')
    print(jobs)


# 获取某个job最后一次构建的配置
def test_jenkins_job_config():
    server = autojenkins.Jenkins(url="http://192.168.150.191:8080/jenkins/", username="admin", password="admin")

    name = 'web-ui-test'

    job_info = server.get_job_info(name)
    pprint.pprint(job_info.buildable)
    pprint.pprint(job_info.build_stability)
    pprint.pprint(job_info.last_build.url)
    pprint.pprint(job_info.build_params.default_parameter_values)

    pprint.pprint(job_info.build_params.parameter_defines)
    pprint.pprint(job_info.last_build.nubmer)
    pprint.pprint(job_info.last_build.url)


def test_jenkins_build_info():
    server = autojenkins.Jenkins(url="http://10.199.132.55:8181/jenkins/", username="admin", password="admin")
    name = 'api-test-xqy-finance'

    job_info = server.get_job_info(name)

    lastbuild_number = job_info.last_build.nubmer
    build_info = server.get_build_info(name, lastbuild_number)
    pprint.pprint(build_info.asdict)
    pprint.pprint(build_info.url)
    pprint.pprint(build_info.action.cause) # Started by timer
    pprint.pprint(build_info.action.parameters) # Started by timer
    pprint.pprint(build_info.duration) # '00:00:01'
    pprint.pprint(build_info.timestamp) # '21小时前'
