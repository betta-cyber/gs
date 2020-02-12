# -*- coding: utf-8 -*-
"""
Created on 2019/6/10 16:27

@description:

@file: script_engine.py

@author: lutianyang5@hivision.com.cn

@version: 0.1
"""

import os
import abc
import uuid
import tempfile
import shlex
import pathlib
import subprocess

from typing import Optional
from .fastlogger import getloggerfast

logger = getloggerfast(__name__)


class IScritEngine(metaclass=abc.ABCMeta):
    def __init__(self):
        self.timeout = 10

    @abc.abstractmethod
    def execute(self, script: str, timeout: int):
        """"""

    @property
    def stdout(self):
        return None

    @property
    def stderr(self):
        return None


class SubprocessEngine(IScritEngine):

    def __init__(self):
        super().__init__()
        self.ret: Optional[subprocess.CompletedProcess] = None

    def runCommand(self, cmd):
        si = subprocess.STARTUPINFO(wShowWindow=0)
        if not self.timeout or self.timeout <= 0:
            self.timeout = 10
        try:
            self.ret = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                      timeout=self.timeout,
                                      startupinfo=si)
            return True
        except Exception as e:
            logger.error(e, exc_info=True)
            return False

    @property
    def stderr(self):
        return self.ret.stderr.strip()

    @property
    def stdout(self):
        return self.ret.stdout.strip()


class CMDEngine(SubprocessEngine):
    EXECUTOR = 'cmd.exe'
    SUBFIX = '.bat'

    def execute(self, script: str, timeout: int):
        self.timeout = timeout
        tmp_dir = tempfile.gettempdir()
        tmp_file: pathlib.Path = pathlib.Path(tmp_dir) / (str(uuid.uuid1()) + self.SUBFIX)
        tmp_file.write_bytes(script.encode())
        res = self.runCommand(str(tmp_file.absolute()))
        os.remove(str(tmp_file))
        return res


class VBSEngine(CMDEngine):
    SUBFIX = '.vbs'
    EXECUTOR = 'cscript //NOLOGO'

    def runCommand(self, cmd):
        _cmd = f'{self.EXECUTOR} {cmd}'
        return super().runCommand(_cmd)


if __name__ == '__main__':
    pass
