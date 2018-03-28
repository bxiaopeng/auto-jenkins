# -*- coding:utf-8 -*-

"""
<Auto Jenkins for human> (api.py)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Created by bixiaofan <wirelessqa@163.com> on 2018/3/23 at 下午3:59
"""

import socket

import jenkins as jenkins_api
from . import utils


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
        return self.BuildInfo(self.jobinfo['last_completed_build'])

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

    @property
    def default_parameter_values(self) -> dict or None:
        """
        默认参数值
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
        """参数定义"""

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


class BuildInfo:
    def __init__(self, buildinfo: dict):
        self.buildinfo = buildinfo

    @property
    def nubmer(self):
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
                    self._parameters.update({param['name']: param['value']})
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
    def remote_urls(self) -> list:
        """仓库地址"""
        return self._remote_urls
