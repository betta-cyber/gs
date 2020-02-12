# -*- coding: utf-8 -*-
"""
Created on 2019/7/9 15:27

@description:

@file: controller.py

@author: lutianyang5@hivision.com.cn
@author: qiulijun@hikvision.com.cn

@version: 0.1
"""

from typing import Optional, List
from core import xmlparse, datacontext, render, fastlogger
import re

logger = fastlogger.getloggerfast(__name__)


class TaskController(object):
    def __init__(self):
        self._datacontext = datacontext.DataController()
        self._render = render.SafeCheckerRender()
        self._xmlparse: Optional[xmlparse.XmlParser] = None
        self._check_items: List[datacontext.CheckItem] = []
        self._win_flag = None
        self.sys_version = ""

    def convertxml_to_report(self, in_xmlfile, out_reportfile):
        """
        转换xml文档到输出的报告文档

        :param in_xmlfile:
        :param out_reportfile:
        :return:
        """

        self._check_items.clear()

        self._xmlparse = xmlparse.XmlParser(in_xmlfile)
        self._xmlparse.parse()
        for item in self._xmlparse.items:
            if item.exception:
                continue
            if str(item.flag) == "10048":
                pattern = r'(\d{1,2}\.){2}\d+'
                self._win_flag = re.search(pattern, str(item.value)).group()
                win_ver_flag_1 = int(self._win_flag.split('.')[0])
                win_ver_flag_2 = int(self._win_flag.split('.')[1])
                self.sys_version = f"{win_ver_flag_1}.{win_ver_flag_2}"
            else:
                pass
        with self._datacontext as session:
            for item in self._xmlparse.items:
                if item.exception:
                    continue
                check_item = self._convert_xmlitem_to_checkitem(item)
                if check_item:
                    self._check_items.append(check_item)
        self._render.render(self._check_items)
        self._render.savetofile(out_reportfile)
        check_res = self.parser_result()
        return check_res

    def _convert_xmlitem_to_checkitem(self, xml_item: xmlparse.GmXmlItem):
        """
        convert xml [GmXmlItem] to [CheckItem]
        :param xml_item:GmXmlItem
        :return: CheckItem
        """
        try:
            checkitem = self._datacontext.session.query(datacontext.CheckItem).filter(
                datacontext.CheckItem.UnionId == xml_item.flag).one_or_none()
        except Exception as e:
            logger.debug(e)
        if checkitem:
            checkitem.check_scanout_log(xmlout=xml_item.value, sys_version=self.sys_version)
        return checkitem

    def parser_result(self):

        check_result = {"high": 0, "medium": 0, "low": 0}
        for item in self._check_items:
            if int(item.mPassed) == 0:
                if item.Level == "High":
                    check_result["high"] += 1

                elif item.Level == "Medium":
                    check_result["medium"] += 1
                else:
                    check_result["low"] += 1
            else:
                pass
        return check_result

    def update_item(self, items_result):
        # 区分Windows系统，控制补丁误报情况
        for item in items_result:
            win_ver_flag_1 = int(self._win_flag.split('.')[0])
            win_ver_flag_2 = int(self._win_flag.split('.')[1])
            self.sys_version = f"{win_ver_flag_1}.{win_ver_flag_2}"
            if win_ver_flag_1 == 10:
                # Win10
                if str(item.UnionId) in ["10037", "10038", "10039"]:
                    item.mPassed = 1
                else:
                    pass
            elif win_ver_flag_1 == 6 and win_ver_flag_2 >= 2:
                # win8,server2012版本,不受ms12-020,CVE-2019-0708漏洞影响
                if str(item.UnionId) in ["10039", "10037"]:
                    item.mPassed = 1
            elif win_ver_flag_1 == 6 and win_ver_flag_2 == 1:
                # win7及server2008版本
                pass
            elif win_ver_flag_1 == 5:
                # xp vista
                if str(item.UnionId) in ["10049"]:
                    item.mPassed = 1
            else:
                pass
            if str(item.UnionId) == "10048":
                # 报表中不显示检测用户操作系统检测项
                continue
            self._check_items.append(item)


if __name__ == '__main__':
    pass
