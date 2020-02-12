# -*- coding:utf-8 -*-

# 引入需要的模块
import os.path
import json
import datetime
import time
from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
from tornado.options import define, options, parse_command_line
from tornado.escape import json_decode, json_encode, utf8
from tornado.httpserver import HTTPServer
from model import DBSession, Task
from huey_task import linux_check_task, windows_check_task

# 定义变量
define("port", default=8000, help="默认端口8000")


# 创建视图类
class IndexHandler(RequestHandler):
    def get(self):
        self.render("index.html")


class TaskHandler(RequestHandler):
    def get(self):
        session = DBSession()
        tasks = session.query(Task).filter().all()
        res = []
        for t in tasks:
            time_str = t.update_time.strftime('%Y-%m-%d %H:%M:%S')
            data = {'task_id': t.task_id, 'ip': t.ip, 'status': t.status, 'update_time': time_str, 'op_user': t.op_user, 'os': t.os}
            res.append(data)
        self.render("task.html", tasks=res)
        # result = dict(result=res, status=True, code=200)
        # self.write(json_encode(result))

    def post(self, *args, **kwargs):
        post_data = self.request.body_arguments
        post_data = {x: post_data.get(x)[0].decode("utf-8") for x in post_data.keys()}
        if not post_data:
            post_data = self.request.body.decode('utf-8')
            post_data = json.loads(post_data)

            if post_data['os'] == "linux":
                session = DBSession()
                task_id_str = "gcheck_" + post_data['ip'] + "_" + str(int(time.time()))
                task = Task(task_id=task_id_str, ip=post_data['ip'], port=post_data['port'], os='linux',
                            username=post_data['username'], password=post_data['password'], status='init', op_user='admin',
                            update_time=datetime.datetime.now())
                session.add(task)
                session.commit()
                session.close()

                # add task
                linux_check_task(task_id_str)

                result = dict(result='generate task success', status=True, code=200)
                self.write(json_encode(result))
            else:
                session = DBSession()
                task_id_str = "gcheck_" + post_data['ip'] + "_" + str(int(time.time()))
                task = Task(task_id=task_id_str, ip=post_data['ip'], port="default", os='windows',
                            username=post_data['username'], password=post_data['password'], status='init', op_user='admin',
                            update_time=datetime.datetime.now())
                session.add(task)
                session.commit()
                session.close()

                # add task
                windows_check_task(task_id_str)

                result = dict(result='generate task success', status=True, code=200)
                self.write(json_encode(result))

    def delete(self, *args, **kwargs):
        post_data = self.request.body_arguments
        post_data = {x: post_data.get(x)[0].decode("utf-8") for x in post_data.keys()}
        if not post_data:
            post_data = self.request.body.decode('utf-8')
            post_data = json.loads(post_data)

        try:
            session = DBSession()
            session.query(Task).filter_by(task_id=post_data['task_id']).delete()
            session.commit()
            session.close()

            result = dict(result='delete task success', status=True, code=200)
            self.write(json_encode(result))
        except Exception as e:
            result = dict(result='delete task fail', status=True, code=200)
            self.write(json_encode(result))


class TaskReportHandler(RequestHandler):
    def get(self):
        task_id = self.get_argument('id')
        session = DBSession()
        task = session.query(Task).filter_by(task_id=task_id).first()
        if task.os == "linux":
            self.render("..\\html\\%s_result_linux.html" % task.task_id)
        else:
            self.render("..\\html\\%s_result.html" % task.task_id)


# 程序入口
if __name__ == '__main__':
    # 开始监听
    parse_command_line()
    app = Application(
        [
            (r'/', IndexHandler),
            (r'/task', TaskHandler),
            (r'/task_report', TaskReportHandler)
        ],

        # 项目配置信息
        # 网页模板
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        # 静态文件
        static_path=os.path.join(os.path.dirname(__file__), "static"),

        debug=True
    )

    # 部署
    server = HTTPServer(app)
    server.listen(options.port)

    # 轮询监听
    IOLoop.current().start()
