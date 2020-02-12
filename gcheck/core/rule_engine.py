# -*- coding: utf-8 -*-
"""
Created on 2019/6/11 10:53

@description:

@file: rule_engine.py

@author: lutianyang5@hivision.com.cn

@version: 0.1
"""
import abc
import regex


class IRuleEngine(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def verify(self, rule, result) -> int:
        """"""


class RegexEngine(IRuleEngine):
    def verify(self, rule, result) -> int:
        return len(regex.findall(rule, result))


if __name__ == '__main__':
    pass
