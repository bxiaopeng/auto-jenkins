# -*- coding:utf-8 -*-

"""
<Description> (test_filter_jenkins_url.py)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Created by bixiaofan <wirelessqa@163.com> on 2018/7/17 at 下午1:52
"""
from auto_jenkins.core import _split_jenkins_url_job_name


def test_has_view():
    has_view = "http://10.199.132.55:8181/jenkins/view/apitest/job/api-test-hs-invoice/"
    jenkins_url, job_name = _split_jenkins_url_job_name(has_view)
    assert "http://10.199.132.55:8181/jenkins" == jenkins_url
    assert "api-test-hs-invoice" == job_name

def test_no_view():
    no_view = "http://10.199.132.55:8181/jenkins/job/api-test-hs-invoice/"
    jenkins_url, job_name = _split_jenkins_url_job_name(no_view)
    assert "http://10.199.132.55:8181/jenkins" == jenkins_url
    assert "api-test-hs-invoice" == job_name