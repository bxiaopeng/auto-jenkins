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
    """通过 job url 直接获取 job info"""
    job_info = auto_jenkins.get_job_info("http://10.199.132.55:8181/jenkins/job/api-test-xqy-finance/",
                                         username="admin",
                                         password="admin")

    assert job_info.url == "http://10.199.132.55:8181/jenkins/job/api-test-xqy-finance/"
    assert job_info.name == "api-test-xqy-finance"

    pprint.pprint(job_info.last_failed_build.url)
    pprint.pprint(job_info.last_failed_build.number)
    pprint.pprint(job_info.last_successful_build.url)
    pprint.pprint(job_info.last_successful_build.number)
    pprint.pprint(job_info.last_completed_build.url)
    pprint.pprint(job_info.last_completed_build.number)
    pprint.pprint(job_info.last_build.number)
    pprint.pprint(job_info.last_build.url)


def test_get_server():
    server, job_name = auto_jenkins.connect_job("http://10.199.132.55:8181/jenkins/api-test-xqy-finance",
                                                username="admin",
                                                password="admin")

    job_info = server.get_job_info(job_name)
    print(job_info.name)


# def test_get_build_params_defines():
#     # server = auto_jenkins.server("http://10.199.132.55:8181/jenkins/api-test-xqy-finance",
#     #                              username="admin",
#     #                              password="admin")
#     server = auto_jenkins.server("http://192.168.150.191:8080/jenkins/job/web-test-xqy-all",
#                                  username="admin",
#                                  password="admin")
#
#     # 构建带参数 api-test-xqy-finance 任务，接受不同类型的参数
#     # server.build_job('api-test-xqy-finance',
#     #                  {
#     #                      'env': 'test',
#     #                      'module': "finance",
#     #                      'plevel': "p4"
#     #                  }
#     #                  )
#
#     # time.sleep(10)  # 等任务构建完，请自行调整时间
#
#     name = 'web-test-xqy-all'
#
#     job_info = server.get_job_info(name)
#     print(job_info.build_params.default_parameter_values)
#     parameter_defines = job_info.build_params.parameter_defines
#
#     param_infos = []
#     for param in parameter_defines:
#
#         print(param)
#         param_name= param.get("name")
#         print(param_name)
#         param_type = param.get("type")
#         print(param_type)
#         param_description = param.get("description")
#
#         new_param_type = ""
#         param_values = ""
#
#         if param_type == "ChoiceParameterDefinition":
#             param_values = param.get("choices")
#             new_param_type = "choices"
#         elif param_type == "PasswordParameterDefinition":
#             new_param_type = "password"
#         elif param_type == "StringParameterDefinition":
#             new_param_type = "string"
#
#
#         default_value = param.get("default_param_value").get("value")
#
#         new_param = {"name":param_name,"description":param_description,"type":new_param_type,"values":param_values,"default_value":default_value}
#         param_infos.append(new_param)
#
#     print(param_infos)

def test_get_build_params_defines():
    """测试获取定义的参数信息列表"""
    server, job_name = auto_jenkins.connect_job("http://10.199.132.55:8181/jenkins/job/api-test-xqy-finance",
                                                username="admin",
                                                password="admin")

    print(server.get_job_info(job_name).build_params.defines)
    job_info = server.get_job_info(job_name)

    print(job_info.last_build.number)

    queue_item = server.build_job(job_name,
                                  parameters={
                                      'env': "test",
                                      'module': "finance",
                                      'plevel': "p1"
                                  })
    print(job_info.is_in_queue)
    print(job_info.buildable)

    print(job_info.next_build_number)
    # pprint.pprint(job_info.jobinfo)

    # pprint.pprint(server.get_build_info("api-test-xqy-finance", job_info.next_build_number).buildinfo)


def test_get_build_params_defines_profile():
    """测试获取定义的参数信息列表(性能测试那个)"""
    server, job_name = auto_jenkins.connect_job("http://10.98.17.52:8082/jenkins/job/xqy_jmeter_test/",
                                                username="admin",
                                                password="xqy_admin")

    pprint.pprint(server.get_job_info(job_name).build_params.defines)

    parameters = {
        'api': "",
        'jmx_path': '',
        'times': '',
        'period': ''
    }
    # server.build_job()

    job_info = server.get_job_info(job_name)
    print(job_info.last_build.number)


def test_build_job():
    """测试获取定义的参数信息列表"""
    server, job_name = auto_jenkins.connect_job("http://10.199.132.55:8181/jenkins/view/apitest/job/api-test-uc/",
                                                username="admin",
                                                password="admin")

    print(server.get_job_info(job_name).build_params.defines)

    parameters = {
        'env': "test"
    }
    server.build_job(job_name, parameters)


def test_build_job_checkbox():
    """构建任务的参数是 checkbox """
    server, job_name = auto_jenkins.connect_job("http://10.199.132.55:8181/jenkins/job/api-test-xxb-jzjf/",
                                                username="admin",
                                                password="admin")

    pprint.pprint(server.get_job_info(job_name).build_params.defines)
    pprint.pprint(server.get_job_info(job_name).build_params.default_parameter_values)

    # parameters = {
    #     'env': "test"
    # }
    # server.build_job("api-test-xxb-jzjf",{'env': 'test', 'plevel': 'all', 'groups': '"wlqd,invoie'})


def test_build_job_no_param():
    """构建任务无构建参数"""
    server, job_name = auto_jenkins.connect_job("http://192.168.110.173:8080/jenkins/job/invoice-api-test/",
                                                username="admin",
                                                password="hswy")

    pprint.pprint(server.get_job_info(job_name).build_params.default_parameter_values)
