# -*- coding:utf-8 -*-

"""
<Description> (test_build_params.py)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Created by bixiaofan <wirelessqa@163.com> on 2018/7/18 at 下午2:15
"""
import pprint
import re

from auto_jenkins import connect_job


def test_build_job_checkbox():
    """构建任务的参数是 checkbox """
    server, job_name = connect_job("http://10.199.132.55:8181/jenkins/job/bixiaopeng_demo/",
                                                username="admin",
                                                password="admin")

    # pprint.pprint(server.get_job_info(job_name).build_params.defines)
    # pprint.pprint(server.get_job_info(job_name).build_params.default_parameter_values)

    # default_config = server.get_job_config(job_name)
    #
    # # 从默认配置中找到要被替换的一整行内容
    # be_replace =  "<defaultValue>" + re.findall(r"<defaultValue>(.+?)</defaultValue>", default_config)[0] +"</defaultValue>"
    # # 用新的内容替换
    # replaces = '<defaultValue>wlqd,invoie,printExpress</defaultValue>'
    #
    # # 替换
    # new_config = default_config.replace(be_replace,replaces)
    #
    # # 重新替换
    # server.reconfig_job(job_name,new_config)


    # parameters = {
    #     'env': "test"
    # }
    server.build_checkbox_job(job_name, {'env': 'test', 'plevel': 'all'},checkbox="wlqd")


def test_build_job_no_param():
    """构建任务无构建参数"""
    server, job_name = connect_job("http://192.168.110.173:8080/jenkins/job/invoice-api-test/",
                                                username="admin",
                                                password="hswy")

    pprint.pprint(server.get_job_info(job_name).build_params.default_parameter_values)
