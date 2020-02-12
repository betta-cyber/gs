# -*- coding: utf-8 -*-
"""
Created on 2019/7/5 17:18

@description:

@file: render.py

@author: lutianyang5@hivision.com.cn

@version: 0.1
"""

import os
import jinja2
import pathlib
from typing import List, Optional

from core import datacontext


class SafeCheckerRender(object):
    TEMPLATE_NAME = 'template_report.html'
    TEMPLATE_ADVANCED_NAME = 'directory_report.html'
    TEMPLATE_DIR = 'templates'

    def __init__(self, report_type=None):
        workdir = pathlib.Path(os.getcwd())

        self._fileloader = jinja2.FileSystemLoader(
            [self.TEMPLATE_DIR, workdir / self.TEMPLATE_DIR, workdir.parent / self.TEMPLATE_DIR])
        self._envfounder = jinja2.Environment(loader=self._fileloader)
        if report_type:
            self._render_jinja2 = self._envfounder.get_template(self.TEMPLATE_ADVANCED_NAME)
        else:
            self._render_jinja2 = self._envfounder.get_template(self.TEMPLATE_NAME)
        self.result: Optional[str] = None
        self.result_file: Optional[pathlib.Path] = None

    def render(self, items: List[datacontext.CheckItem]):
        self.result = self._render_jinja2.render(items=items)
        return self.result

    def savetofile(self, filepos):
        self.result_file = pathlib.Path(filepos)
        with self.result_file.open('wb') as fh:
            fh.write(self.result.encode())
        return self.result_file


if __name__ == '__main__':
    pass
