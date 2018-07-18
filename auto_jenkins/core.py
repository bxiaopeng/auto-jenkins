# -*- coding:utf-8 -*-

"""
<Auto Jenkins for human> (api.py)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Created by bixiaofan <wirelessqa@163.com> on 2018/3/23 at 下午3:59
"""

import jenkins as jenkins_api
import pprint
import re
import socket
from furl import furl

from . import utils


def _split_jenkins_url_job_name(job_url: str):
    """从job url中分离 jenkins url and job name"""
    f = furl(job_url)
    segments = f.path.segments

    if str(job_url).endswith("/"):
        job_name = segments[-2]
    else:
        job_name = segments[-1]

    f.path = "jenkins"

    return str(f), job_name


def is_valid_job(job_url: str, username: str = None, password: str = None) -> bool:
    """ 判断jenkins job 是否有效"""
    jenkins_url, job_name = _split_jenkins_url_job_name(job_url)

    try:
        job_info = Jenkins(jenkins_url, username, password).get_job_info(job_name)
    except Exception:
        return False
    return job_info.displayname is not None


def get_job_info(job_url: str, username=None, password=None):
    jenkins_url, job_name = _split_jenkins_url_job_name(job_url)
    try:
        server, _ = connect_job(jenkins_url, username, password)
        return server.get_job_info(job_name)
    except:
        return None


def connect_job(job_url: str, username: str = None, password: str = None):
    """
    通过job url 获取 server 和 job name
    :param job_url: JOB 的 URL 地址
    :param username: 用户名
    :param password: 密码
    :return:         server,job_name
    """
    jenkins_url, job_name = _split_jenkins_url_job_name(job_url)
    return Jenkins(jenkins_url, username, password), job_name


def connect_jenkins(jenkins_url: str, username: str = None, password: str = None):
    """
    连接 jenkins
    :param jenkins_url:
    :param username:
    :param password:
    :return:
    """
    return Jenkins(jenkins_url, username, password)


class Jenkins(jenkins_api.Jenkins):
    def __init__(self, url, username=None, password=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
        super().__init__(url, username, password, timeout)

    def get_job_info(self, name: str, depth: int = 0, fetch_all_builds: bool = False):
        """
        获取任务信息
        :param name: 任务名
        :param depth: 深度，默认为 0
        :param fetch_all_builds: 是否获取所有构建，默认为 Flase
        :return: JobInfo 对象
        """
        try:
            jobinfo = super().get_job_info(name, depth, fetch_all_builds)
        except jenkins_api.NotFoundException:
            raise Exception("{} 任务没有找到".format(name))

        return JobInfo(jobinfo)

    def get_build_info(self, name: str, number: int, depth=0):

        buildinfo = super().get_build_info(name, number, depth)

        return BuildInfo(buildinfo)

    def build_checkbox_job(self, job_name, params: dict, checkbox: str):
        """
        构建有多选框的任务，因为多选框是通过插件获得的功能，直接传入参数不能被接收，因此通过配置默认参数来解决这个问题。
        :param job_name:
        :param params:     不包括 checkbox 参数的字典,如：{'env': 'test', 'plevel': 'all'}
        :param checkbox:   checkbox 的值，如:"one,two"

        例:
        server.build_checkbox_job(job_name, {'env': 'test', 'plevel': 'all'},checkbox="wlqd")
        """
        default_config = self.get_job_config(job_name)
        # 从默认配置中找到要被替换的一整行内容
        be_replace = "<defaultValue>" + re.findall(r"<defaultValue>(.+?)</defaultValue>", default_config)[
            0] + "</defaultValue>"
        # 用新的内容替换
        replaces = '<defaultValue>{}</defaultValue>'.format(checkbox)

        # 替换
        new_config = default_config.replace(be_replace, replaces)

        try:
            # 重新替换
            self.reconfig_job(job_name, new_config)

            self.build_job(job_name, params)
        finally:
            # 还原配置
            self.reconfig_job(job_name, default_config)


class JobInfo:
    def __init__(self, jobinfo):
        self.jobinfo = jobinfo

    @property
    def buildable(self) -> bool:
        """是否可用"""
        return self.jobinfo['buildable']

    @property
    def builds(self) -> list:
        """构建历史记录"""
        return self.jobinfo['builds']

    @property
    def color(self):
        """构建状态"""
        return self.jobinfo['color']

    @property
    def is_concurrent_build(self) -> bool:
        """是否并发构建"""
        return self.jobinfo['concurrentBuild']

    @property
    def description(self) -> str:
        """任务描述"""
        return self.jobinfo['description']

    @property
    def displayname(self) -> str:
        """显示名称"""
        return self.jobinfo['displayName']

    @property
    def full_displayname(self) -> str:
        """显示全名"""
        return self.jobinfo['fullDisplayName']

    @property
    def health_report(self) -> list:
        """
        健康报告

        example:

            [
            {'description': 'Build stability: 1 out of the last 3 builds failed.',
              'iconClassName': 'icon-health-60to79',
              'iconUrl': 'health-60to79.png',
              'score': 66
            }
            ],
        """
        return self.jobinfo['healthReport']

    @property
    def build_stability(self) -> str:
        """构建稳定性

        :return e.g. 'Build stability: 1 out of the last 3 builds failed.'

        """
        return self.health_report[0]['description']

    @property
    def score(self) -> int:
        """健康得分"""
        return self.health_report[0]['score']

    @property
    def is_in_queue(self) -> bool:
        """是否在队列中"""
        return self.jobinfo['inQueue']

    @property
    def last_build(self):
        """
        最近一次构建的信息

        example:
            {'_class': 'hudson.model.FreeStyleBuild',
             'number': 21,
             'url': 'http://10.199.138.55:9181/jenkins/job/justtest/21/'
             }
        """
        return self.BuildInfo(self.jobinfo['lastBuild'])

    @property
    def last_completed_build(self):
        """最近一次完整构建"""
        return self.BuildInfo(self.jobinfo['lastCompletedBuild'])

    @property
    def last_failed_build(self):
        return self.BuildInfo(self.jobinfo['lastFailedBuild'])

    @property
    def last_stable_build(self):
        return self.BuildInfo(self.jobinfo['lastStableBuild'])

    @property
    def last_successful_build(self):
        return self.BuildInfo(self.jobinfo['lastSuccessfulBuild'])

    @property
    def last_unstable_build(self):
        return self.BuildInfo(self.jobinfo['lastUnstableBuild'])

    @property
    def last_unsuccessful_build(self):
        return self.jobinfo['lastUnsuccessfulBuild']

    @property
    def name(self):
        """任务名"""
        return self.jobinfo['name']

    @property
    def next_build_number(self) -> int:
        """下一个构建号"""
        return self.jobinfo['nextBuildNumber']

    @property
    def build_params(self):
        """构建的配置"""
        return BuildParameters(self.jobinfo['property'])

    @property
    def url(self) -> str:
        """job url"""
        return self.jobinfo['url']

    @property
    def upstream_projects(self) -> list:
        """上游项目"""
        return self.jobinfo['upstreamProjects']

    @property
    def scm(self) -> dict:
        """
        example:
             {'_class': 'hudson.plugins.git.GitSCM'}

        """
        return self.jobinfo['scm']

    @property
    def asdict(self) -> dict:
        return self.jobinfo

    class BuildInfo:
        def __init__(self, buildinfo: dict):
            self.buildinfo = buildinfo

        @property
        def number(self):
            """构建号"""
            try:
                return self.buildinfo['number']
            except:
                return None

        @property
        def url(self):
            """构建地址"""
            try:
                return self.buildinfo['url']
            except:
                return None


class BuildParameters:
    def __init__(self, buildparams):
        self.buildparams = buildparams

        pprint.pprint(buildparams)

    @property
    def default_parameter_values(self) -> dict or None:
        """
        获取任务构建的默认参数值
        :return  e.g. [{'severity':"block"},]
        """

        if self.parameter_defines:
            _default_parameter_values = {}

            for a_paramdefine in self.parameter_defines:
                name = a_paramdefine['default_param_value']['name']
                try:
                    value = a_paramdefine['default_param_value']['value']
                except KeyError:
                    value = None
                _default_parameter_values.update({name: value})
            return _default_parameter_values

        else:
            return None

    @property
    def parameter_defines(self) -> list:
        """获取构建参数的定义"""

        paramdefines = []

        for bp in self.buildparams:

            if bp['_class'] == "hudson.model.ParametersDefinitionProperty":
                paramdefines = bp['parameterDefinitions']

        new_paramdefines = []

        if paramdefines:

            for pdf in paramdefines:
                name = pdf['name']
                description = pdf['description']
                type = pdf['type']
                default_param_value = pdf['defaultParameterValue']

                choices = []
                if type == 'ChoiceParameterDefinition':
                    choices = pdf['choices']

                paramdefine = {'name': name, 'description': description, 'type': type,
                               'default_param_value': default_param_value}

                if choices:
                    paramdefine.update({'choices': choices})

                new_paramdefines.append(paramdefine)

        return new_paramdefines

    @property
    def defines(self) -> list:
        """获取构建参数的定义，并格式化参数类型

        格式化后的参数类型：
        字符串 -> string
        选择 -> choices
        复选框 -> checkbox

        usage:
        server.get_job_info("job_name").build_params.defines

        return：
        [{'name': 'test', 'description': '指定测试路径', 'type': 'string', 'values': '', 'default_value': 'tests/'},]

        如果为空，则返回 []
        """
        parameter_defines = self.parameter_defines

        # pprint.pprint(parameter_defines)

        param_infos = []
        for param in parameter_defines:
            param_name = param.get("name")
            param_type = param.get("type")
            param_description = param.get("description")

            new_param_type = ""
            param_values = ""

            if param_type == "ChoiceParameterDefinition":
                param_values = param.get("choices")
                new_param_type = "choices"
            elif param_type == "PasswordParameterDefinition":
                new_param_type = "password"
            elif param_type == "StringParameterDefinition":
                new_param_type = "string"
            elif param_type == "PT_CHECKBOX":
                new_param_type = "checkbox"
            elif param_type == "PT_SINGLE_SELECT":
                new_param_type = "single_select"

            default_value = param.get("default_param_value")

            if default_value:
                default_value = param.get("default_param_value").get("value")

            param_infos.append({"name": param_name,
                                "description": param_description,
                                "type": new_param_type,
                                "values": param_values,
                                "default_value": default_value
                                })

        return param_infos


class BuildInfo:
    def __init__(self, buildinfo: dict):
        self.buildinfo = buildinfo

    @property
    def number(self):
        """构建号"""
        try:
            return self.buildinfo['number']
        except:
            return None

    @property
    def url(self):
        """构建地址"""
        try:
            return self.buildinfo['url']
        except:
            return None

    @property
    def asdict(self):
        return self.buildinfo

    @property
    def action(self):
        return BuildAction(self.buildinfo['actions'])

    @property
    def duration(self) -> str:
        """构建持续时间"""

        try:
            return utils.ms2hms(self.buildinfo['duration'] / 1000)
        except:
            return "0"

    @property
    def start_time(self) -> str:
        """构建开始时间"""
        try:
            return utils.humanize(self.buildinfo['timestamp'] / 1000)
        except:
            return self.buildinfo['timestamp']

    @property
    def result(self):
        return self.buildinfo['result']

    @property
    def artifacts(self) -> list:
        """
        构建产物
        :return:

        如：[{'displayPath': 'allure-report.zip',
                'fileName': 'allure-report.zip',
                'relativePath': 'allure-report.zip'}]
        """
        return self.buildinfo['artifacts']

    @property
    def is_building(self) -> bool:
        """是否正在构建"""
        return self.buildinfo['building']

    @property
    def change_set(self) -> dict:
        """代码变更"""
        return self.buildinfo['changeSet']

    @property
    def id(self) -> int:
        return self.buildinfo['id']

    @property
    def name(self) -> str:
        return self.buildinfo['name']


class BuildAction:
    def __init__(self, actions):
        self.actions = actions
        self._cause = None
        self._parameters = {}
        self._by_branch_names = None

        for action in self.actions:

            _class = None

            try:
                _class = action['_class']
            except:
                pass
            if _class == 'hudson.model.CauseAction':
                self._cause = action['causes'][0]['shortDescription']  # 'shortDescription': 'Started by timer'

            elif _class == 'hudson.model.ParametersAction':
                for param in action['parameters']:
                    try:
                        self._parameters.update({param['name']: param['value']})
                    except:
                        pass
            elif _class == 'hudson.plugins.git.util.BuildData':
                self._by_branch_names = action['buildsByBranchName']
                self._remote_urls = action['remoteUrls']

    @property
    def cause(self) -> str:
        """如何触发的构建
        :return 构建的原因

        如：Started by timer(定时)
        """
        return self._cause

    @property
    def parameters(self) -> dict:
        """构建时的参数配置

        :return 参数字典

        如：{'env': 'test', 'browser': 'chrome'}
        """
        return self._parameters

    @property
    def by_branch_names(self) -> dict:
        """分支信息"""
        return self._by_branch_names

    @property
    def remote_urls(self) -> list or None:
        """仓库地址"""
        try:
            return self._remote_urls
        except Exception:
            return None
