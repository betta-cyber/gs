# -*- coding: utf-8 -*-
"""
Created on 2019/7/5 21:44

@description:

@file: xmlparse.py

@author: lutianyang5@hivision.com.cn

@version: 0.1
"""
import pathlib
from lxml import etree
from typing import Optional, List


class GmXmlItem:
    flag: Optional[str] = None
    command: Optional[str] = None
    value: Optional[str] = None
    exception: Optional[Exception] = None

    def __init__(self, xmlnode):
        self._xmlnode: etree._Element = xmlnode
        try:
            self.flag = self._xmlnode.attrib.get('flag')
            self.command = self._xmlnode.find('.//command').text.strip()
            self.value = self._xmlnode.find('.//value').text.strip()
        except Exception as e:
            self.exception = e


class XmlParser(object):
    TARTGETPATH = './/item'
    MSGPATH = './/msg'

    def __init__(self, filepath):
        self._xmlfile = pathlib.Path(filepath)
        if not self._xmlfile.exists() or not self._xmlfile.is_file():
            raise FileNotFoundError(self._xmlfile.absolute())

        self._tree = etree.parse(str(filepath))
        self._items: List[GmXmlItem] = list()

    def parse(self) -> List[GmXmlItem]:
        items = self._tree.findall(self.TARTGETPATH)
        self._items.clear()
        self._items.extend(map(lambda itm: GmXmlItem(itm), items))
        return self.items


    @property
    def items(self) -> List[GmXmlItem]:
        return self._items

class MsgParser(object):
    MSGPATH = './/msg'

    def __init__(self,filepath):
        self._xmlfile = pathlib.Path(filepath)
        if not self._xmlfile.exists() or not self._xmlfile.is_file():
            raise FileNotFoundError(self._xmlfile.absolute())

        self._tree = etree.parse(str(filepath))
        self._res = None

    def parse(self):
        self._res = self._tree.findall(self.MSGPATH)


if __name__ == '__main__':
    pass
