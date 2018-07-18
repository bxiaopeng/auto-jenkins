# -*- coding:utf-8 -*-

"""
<Description> (test_connect.py)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Created by bixiaofan <wirelessqa@163.com> on 2018/7/17 at 下午1:48
"""
import pprint
import pytest

import auto_jenkins

JOB_URL = "http://10.199.132.55:8181/jenkins/job/SyncIris/"
JENKINS_URL = "http://10.199.132.55:8181/jenkins"
JOB_NAME = "SyncIris"


def test_connect():
    # 通过 job url 获取 server 和 job_name
    server, job_name = auto_jenkins.connect_job(JOB_URL)
    assert JOB_NAME == job_name
    defines = server.get_job_info(job_name).build_params.defines

    # 通过 jenkins 获取 server
    server2 = auto_jenkins.connect_jenkins(JENKINS_URL)
    defines2 = server2.get_job_info(JOB_NAME).build_params.defines

    # 直接通过 Jenkins 这个类连接
    server3 = auto_jenkins.Jenkins(JENKINS_URL)
    defines3 = server3.get_job_info(JOB_NAME).build_params.defines

    assert defines == defines2 == defines3

@pytest.mark.skip
def test_connect2():
    # 通过 job url 获取 server 和 job_name
    server, job_name = auto_jenkins.connect_job(JOB_URL)
    assert JOB_NAME == job_name
    build_params = {
        "xqyEnv": "xqy-test",
        "ucEnv": "uc-sit"
    }

    server.build_checkbox_job(job_name,build_params,checkbox="activity,boss")



@pytest.mark.skip
def test_connect3():
    # 通过 job url 获取 server 和 job_name
    server, job_name = auto_jenkins.connect_job("http://10.199.132.55:8181/jenkins/job/SyncIris/")
    assert JOB_NAME == job_name
    build_params = {
        "xqyEnv": "xqy-test",
        "ucEnv": "uc-sit"
    }

    server.build_checkbox_job(job_name,build_params,checkbox="activity,boss")

