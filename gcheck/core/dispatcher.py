# -*- coding: utf-8 -*-
"""
Created on 2019/6/11 11:06

@description:

@file: dispatcher.py

@author: lutianyang5@hivision.com.cn

@version: 0.1
"""

import enum

from . import script_engine, rule_engine


class ScriptDispatch(enum.Enum):
    VBS = script_engine.VBSEngine()
    CMD = script_engine.CMDEngine()
    BAT = script_engine.CMDEngine()

    @staticmethod
    def load(k: str):
        return ScriptDispatch.__dict__.get(k.upper(), None).value


class RuleDispatch(enum.Enum):
    REGEX = rule_engine.RegexEngine()

    @staticmethod
    def load(k: str):
        return RuleDispatch.__dict__.get(k.upper(), None).value



if __name__ == '__main__':
    # ScriptDispatch.__dict__.get('cmd')
    pass
