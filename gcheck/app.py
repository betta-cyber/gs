# -*- coding:utf-8 -*-

# 引入需要的模块
import os.path
import json
import paramiko
from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
from tornado.options import define, options, parse_command_line
from tornado.escape import json_decode, json_encode, utf8
from tornado.httpserver import HTTPServer

# 定义变量
define("port", default=8000, help="默认端口8000")


# 创建视图类
class IndexHandler(RequestHandler):
    def get(self):
        self.render("index.html")


class TaskHandler(RequestHandler):
    def get(self):
        pass

    def post(self, *args, **kwargs):
        post_data = self.request.body_arguments
        post_data = {x: post_data.get(x)[0].decode("utf-8") for x in post_data.keys()}
        if not post_data:
            post_data = self.request.body.decode('utf-8')
            post_data = json.loads(post_data)
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=post_data['ip'], port=22, username=post_data['username'], password=post_data['password'])
            stdin, stdout, stderr = ssh.exec_command('ls')
            result = stdout.read()
            ssh.close()
            result = result.decode('utf-8')
            data = dict(result=result, status=True, code=200)
            self.write(json_encode(data))
        except Exception:
            self.set_status(400)
            result = dict(result='test failed', status=True, code=200)
            self.write(json_encode(result))


class TestHandler(RequestHandler):
    def get(self):
        pass

    def post(self, *args, **kwargs):
        post_data = self.request.body_arguments
        post_data = {x: post_data.get(x)[0].decode("utf-8") for x in post_data.keys()}

        print(post_data)
        if not post_data:
            post_data = self.request.body.decode('utf-8')
            post_data = json.loads(post_data)

        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=post_data['ip'], port=22, username=post_data['username'], password=post_data['password'])
            stdin, stdout, stderr = ssh.exec_command('ls')
            result = stdout.read()
            ssh.close()

            data = dict(result="test ok", status=True, code=200)
            self.write(json_encode(data))
        except Exception:
            self.set_status(400)
            result = dict(result='test failed', status=True, code=200)
            self.write(json_encode(result))


# 程序入口
if __name__ == '__main__':
    # 开始监听
    parse_command_line()
    app = Application(
        [
            (r'/', IndexHandler),
            (r'/task', TaskHandler),
            (r'/test', TestHandler),
        ],

        # 项目配置信息
        # 网页模板
        template_path=os.path.join(os.path.dirname(__file__), "web/dist"),
        # 静态文件
        static_path=os.path.join(os.path.dirname(__file__), "web/dist/static"),

        debug=True
    )

    # 部署
    server = HTTPServer(app)
    server.listen(options.port)

    # 轮询监听
    IOLoop.current().start()
