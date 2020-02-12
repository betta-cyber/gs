# -*- coding:utf-8
# @File     : ssh_sdk.py
# @Author   : qiulijun
# @Date     : 2019/08/12
# @Desc     : linux扫描工具sdk接口
# @Refer    : no
# -----------------------------------------
import os
import paramiko
from core import cfg_lib, fastlogger

logger = fastlogger.getloggerfast(__name__)


class SSHConnection(object):
    _SRC_FILE = cfg_lib.LINUX_SRC_DIR
    _DST_FILE = cfg_lib.LINUX_DST_DIR
    _RES_SRC_FILE = cfg_lib.LINUX_RES_SRC_DIR
    _RES_DST_FILE = cfg_lib.LINUX_RES_DST_DIR

    def __init__(self, login_ip, login_user, login_pass, login_port):
        self.login_ip = login_ip
        self.login_user = login_user
        self.login_pass = login_pass
        self.login_port = login_port
        self.login_timeout = 5
        self.login_flag = None
        self.err_msg = None
        self.__transport = None
        # 初始化进行连接3次尝试，解决账号密码错误，目标ssh未开启检测及端口不对应问题等
        self.login_flag = self.connect

    @property
    def connect(self):
        """
        持久化ssh通道连接
        :return:
        """
        login_flag = False
        try:
            # paramiko.util.log_to_file("log1030.log")
            # 记录paramiko登录失败日志
            trans = paramiko.Transport(((str(self.login_ip)),
                                        int(self.login_port)))
            trans.connect(username=self.login_user,
                          password=self.login_pass)
            self.__transport = trans
            login_flag = True
        except Exception as e:
            logger.debug(e)
            self.error_msg = e
        return login_flag

    def down(self):
        """
        关闭ssh连接
        :return:
        """
        self.__transport.close()

    def run_cmd(self, command, timeout=10):
        """
        远程ssh执行shell命令
        :param command:
        :return:dict
        """
        ssh = paramiko.SSHClient()
        ssh._transport = self.__transport
        # 执行命令,输出错误日志信息
        try:
            stdin, stdout, stderr = ssh.exec_command(command, timeout=int(timeout))
        except Exception as e:
            logger.error(e)
            return
        res = self.byte_to_str(stdout.read())
        error = self.byte_to_str(stderr.read())
        if error.strip():
            return {"flag": False, "res": error}
        else:
            return {"flag": True, "res": res}

    def upload(self):
        """
        启用stfp，将linux检测文件上传至目标服务器进行检测
        :param src_path:
        :param dst_path:
        :return:
        """
        try:
            sftp = paramiko.SFTPClient.from_transport(self.__transport)
        except Exception as e:
            logger.error(e)
            return
        res = self.run_cmd("cd /tmp && pwd")
        if res["flag"]:
            try:
                sftp.put(self._SRC_FILE,
                         self._DST_FILE,
                         confirm=True)
                # 设置八进制权限，使用0o前缀
                sftp.chmod(self._DST_FILE, 0o755)
            except Exception as e:
                logger.error(e)
                return
        else:
            pass

    def download(self, res_dst_file=""):
        """
        启用sftp，输出检测结束后生成的HTML格式报告
        :param server_path:
        :param local_path:
        :return:
        """
        if res_dst_file:
            self._RES_DST_FILE = res_dst_file
        try:
            sftp = paramiko.SFTPClient.from_transport(self.__transport)
        except Exception as e:
            logger.error(e)
            return {"flag": False}
        res = self.run_cmd("cd /tmp && pwd")
        if res["flag"]:
            try:
                sftp.get(self._RES_SRC_FILE, self._RES_DST_FILE)
                return {"flag": True}
            except Exception as e:
                logger.error(e)
                return {"flag": False}
        else:
            return {"flag": False}

    def __close__(self):
        self.down()

    def byte_to_str(self, bytes_data):
        """
        将byte类型转换为str格式
        :param bytes_data
        :return: value
        """
        if isinstance(bytes_data, bytes):
            value = bytes_data.decode("utf-8")
        else:
            value = bytes_data
        return value


if __name__ == '__main__':
    pass
