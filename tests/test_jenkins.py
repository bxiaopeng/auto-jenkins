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

import auto_jenkins


# 获取某个job最后一次构建的配置
def test_jenkins_job_config():
    server = auto_jenkins.Jenkins(url="http://192.168.150.191:8080/jenkins/", username="admin", password="admin")

    name = 'web-test-xqy-all'
    job_info = server.get_job_info(name)
    lastbuild_number = job_info.last_build.number

    build_info = server.get_build_info(name, lastbuild_number)

    pprint.pprint(build_info.action.parameters)  # Started by timer
    pprint.pprint(build_info.action.cause)

    # pprint.pprint(job_info.buildable)
    # pprint.pprint(job_info.build_stability)
    # pprint.pprint(job_info.last_build.url)
    # pprint.pprint(job_info.build_params.default_parameter_values)
    #
    # pprint.pprint(job_info.build_params.parameter_defines)
    # pprint.pprint(job_info.last_build.number)
    # pprint.pprint(job_info.last_build.url)


def test_jenkins_build_info():
    server = auto_jenkins.Jenkins(url="http://10.199.132.55:8181/jenkins/", username="admin", password="admin")
    name = 'api-test-xqy-finance'

    job_info = server.get_job_info(name)

    lastbuild_number = job_info.last_build.number

    print(lastbuild_number)

    build_info = server.get_build_info(name, lastbuild_number)
    pprint.pprint(build_info.asdict)
    pprint.pprint(build_info.url)
    pprint.pprint(build_info.action.cause)  # Started by timer
    pprint.pprint(build_info.action.parameters)  # Started by timer
    pprint.pprint(build_info.duration)  # '00:00:01'
    pprint.pprint(build_info.start_time)  # '21小时前'
    pprint.pprint(build_info.action.remote_urls)  # 'git 址址'
    pprint.pprint(build_info.action.by_branch_names)  # 'git 址址'


def test_is_valid_job():
    assert not auto_jenkins.is_valid_job("http://10.199.132.55:8181/jenkins/job/api-test-peixun2/", "admin", "admin")
    assert auto_jenkins.is_valid_job("http://10.199.132.55:8181/jenkins/job/api-test-peixun/", "admin", "admin")


def test_get_job_info():
    job_info = auto_jenkins.get_job_info("http://10.199.132.55:8181/jenkins/api-test-xqy-finance",
                                         username="admin",
                                         password="admin")

    assert job_info.url == "http://10.199.132.55:8181/jenkins/job/api-test-xqy-finance/"
    assert job_info.name == "api-test-xqy-finance"
