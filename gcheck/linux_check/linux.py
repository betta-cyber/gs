# -*- coding: utf-8 -*-

import time
from core import ssh_connection, fastlogger

logger = fastlogger.getloggerfast(__name__)


class Linux_login(object):
    """
    desc:linux登录验证
    """

    def __init__(self):
        self.user = self.password = self.port = self.ip = None

    def transfer(self, ip="", user="", password="", port=22):
        """
        :param ip:
        :param user:
        :param passowrd:
        :param port:默认为22端口
        :param communicate:
        :return:
        """
        self.ip = ip
        self.user = user
        self.password = password
        self.port = port

    def run(self):
        """
        :return:
        """
        if len(self.ip) == 0 or len(self.user) == 0 or len(self.password) == 0:
            res = "fail"
        else:
            ssh_connector = ssh_connection.SSHConnection(
                self.ip, self.user, self.password, self.port)
            if ssh_connector.login_flag:
                res = "success"
                ssh_connector.__close__()  # 验证后立即断开连接
            else:
                res = "fail"
        return res


class Linux_check(object):
    """
    desc:linux远程下发任务
    """

    def __init__(self, task_id="", ip="", user="", password="", port=22, check_type="linux"):
        """
        :param ip:
        :param user:
        :param passowrd:
        :param port:默认为22端口
        :param communicate:
        :return:
        """
        self.task_id = task_id
        self.ip = ip
        self.user = user
        self.password = password
        self.port = port
        self.check_type = check_type

    def run(self):
        """
        :return:
        """
        res = "error"
        if len(self.ip) == 0 or len(self.user) == 0 or len(self.password) == 0:
            res = "fail"
        else:
            ssh_connector = ssh_connection.SSHConnection(
                self.ip, self.user, self.password, self.port)
            if ssh_connector.login_flag:
                ssh_connector.upload()
                cmd_dic = ssh_connector.run_cmd("cd /tmp && tar -zxvf local_checker_linux.tar.gz", timeout=60)
                time.sleep(5)
                if self.check_type == "linux":
                    cmd = "cd /tmp/local_checker_dist && ./local_checker_linux --catlog Linux"
                elif self.check_type == "tomcat":
                    cmd = f"cd /tmp/local_checker_dist && ./local_checker_linux --catlog Tomcat --dir {self.check_dir}"
                elif self.check_type == "nginx":
                    cmd = f"cd /tmp/local_checker_dist && ./local_checker_linux --catlog Nginx --dir {self.check_dir}"
                res_dic = ssh_connector.run_cmd(cmd, timeout=60)
                logger.debug(res_dic)

                dst_path = "html\\" + self.task_id + "_result_linux.html"
                report_dic = ssh_connector.download(dst_path)
                ssh_connector.__close__()
                if report_dic["flag"]:
                    res = "success"
        return res


if __name__ == "__main__":
    pass
