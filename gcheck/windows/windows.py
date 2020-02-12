# -*- coding: utf-8 -*-

import time
import os
import pathlib
from windows.conn import WindowsMachine
from core import fastlogger, cfg_lib, controller

logger = fastlogger.getloggerfast(__name__)


class Windows_check(object):
    """
    desc:windows检测项下发任务
    """
    # _tomcat_xml_name = cfg_lib.TOMCAT_XML
    # _nginx_xml_name = cfg_lib.NGINX_XML
    # _pgsql_xml_name = cfg_lib.PGSQL_XML
    # _dir_xml_name = cfg_lib.DIRECTORY_XML

    def __init__(self, task_id="", ip="", user="", password="", port=22, check_type="windows"):
        self.check_dir = None
        self.check_config = None
        self.xml_file = None
        self._windows_script_path = cfg_lib.SCRIPT_NAME
        self._windows_pl_dir = cfg_lib.WINDOWS_DIR
        self._windows_xml_name = cfg_lib.WINDOWS_XML

        self.task_id = task_id
        self.ip = ip
        self.user = user
        self.password = password
        self.port = port
        self.check_type = check_type
        self._task_controller = controller.TaskController()

    def run(self):
        if self.check_type == "windows":
            remote_script = os.path.join("c:\\\\", self._windows_script_path)
            cmd = f'cscript //NOLOGO {remote_script}'

            server = WindowsMachine(self.ip, self.user, self.password)
            ret, return_value = server.run_remote(cmd, async=False, output=True)

            self.xml_file = pathlib.Path(self._windows_xml_name)
            if return_value == "success" and self.xml_file.exists():
                if self.xml_file.exists():
                    check_res = self._task_controller.convertxml_to_report(self.xml_file, "html\\" + self.task_id + '_result.html')
                    if check_res:
                        os.remove(self.xml_file)
                    # finish task
                    # need to show task

        elif self.check_type == "tomcat":
            Parser = tomcat_parser.TomcatParser(self.check_dir)
            Parser.start_check()
            self.xml_file = pathlib.Path(self._tomcat_xml_name)
            if self.xml_file.exists():
                check_res = self._task_controller.convertxml_to_report(
                    self.xml_file, "html\\result.html")
        elif self.check_type == "nginx":
            Parser = nginx_parser.NginxParser(self.check_dir)
            Parser.start_check()
            self.xml_file = pathlib.Path(self._nginx_xml_name)
            if self.xml_file.exists():
                check_res = self._task_controller.convertxml_to_report(
                    self.xml_file, "html\\result.html")
                if int(check_res["high"]) > 0 or int(check_res["medium"]) > 0:
                    pass
        elif self.check_type == "postgresql":
            Parser = pgsql_parser.Pgsql_parser(self.check_dir)
            Parser.start_check()
            self.xml_file = pathlib.Path(self._pgsql_xml_name)
            if self.xml_file.exists():
                pass
        # 目录配置敏感文件检测
        elif self.check_type == "directory":
            Parser = diretory_parser.Directory_parser(self.check_config)
            check_res = Parser.start_check()
            if int(check_res) > 0:
                res = f"检测结果：高风险，{int(check_res)}个文件中存在敏感ip信息"
            else:
                res = f"检测结果：安全，所扫描的文件中未存在敏感ip信息"
        else:
            pass
