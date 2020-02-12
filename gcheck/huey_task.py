# -*- coding: utf-8 -*-

# usage:: python venv\\Lib\\site-packages\\huey\\bin\\huey_consumer.py huey_task.huey
# need add
# import pythoncom
# pythoncom.CoInitialize()
# to win32com client dynamic python file to fix 尚未调用 CoInitialize。

from huey import crontab
import json
from huey import RedisHuey
from time import time
from datetime import timedelta, datetime
from windows.windows import Windows_check
from linux_check.linux import Linux_check
from model import DBSession, Task

huey = RedisHuey(host="127.0.0.1", password="")


@huey.task()
def linux_check_task(task_id):
    session = DBSession()
    try:
        task_ins = session.query(Task).filter_by(task_id=task_id).first()
        task_ins.status = "running"
        session.commit()
        task = Linux_check(task_id, task_ins.ip, task_ins.username, task_ins.password, task_ins.port, check_type="linux")
        # run linux task
        task.run()

        # finish task
        task_ins.status = "finish"
        session.commit()
        session.close()
    except Exception as e:
        print(e)
        task_ins.status = "fail"
        session.commit()
        session.close()


@huey.task()
def windows_check_task(task_id):
    session = DBSession()
    try:
        task_ins = session.query(Task).filter_by(task_id=task_id).first()
        task_ins.status = "running"
        session.commit()
        task = Windows_check(task_id, task_ins.ip, task_ins.username, task_ins.password, check_type="windows")
        # a = Windows_check("1111", "10.19.201.88", "administrator", "killer551.", check_type="windows")
        # run windows task
        print(task.run())

        # finish task
        task_ins.status = "finish"
        session.commit()
        session.close()
    except Exception as e:
        print(e)
        task_ins.status = "fail"
        session.commit()
        session.close()
