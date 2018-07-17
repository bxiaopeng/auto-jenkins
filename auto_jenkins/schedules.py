# -*- coding:utf-8 -*-

"""
<Description> (schedules.py)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Created by bixiaofan <wirelessqa@163.com> on 2018/7/4 at 下午4:39
"""


import time

import schedule
import threading

from auto_jenkins import connect_job


def job():
    print("I'm working...")
    # """测试获取定义的参数信息列表"""
    # server = connect_job("http://10.199.132.55:8181/jenkins/view/apitest/job/api-test-uc/",
    #                               username="admin",
    #                               password="admin")
    #
    # print(server.get_job_info("api-test-uc").build_params.defines)
    # parameters = {
    #     'env': "test"
    # }
    # server.build_job("api-test-uc", parameters)


# schedule.every(10).minutes.do(job)
# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)
#
# schedule.every(1).seconds.do(job)
schedule.every(1).seconds.do(job)


def run_continuously(schedule:schedule, interval:int=1)-> threading.Event:
    """
    在子线程循环等待任务的触发
    :param schedule: schedule
    :param interval: 循环等待的间隔时间(秒)
    :return:
    """
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run

run_continuously(schedule)

while True:
    # schedule.run_pending()
    time.sleep(1)
