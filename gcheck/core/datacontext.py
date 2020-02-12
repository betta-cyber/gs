# -*- coding: utf-8 -*-
"""
Created on 2019/6/13 17:17

@description:

@file: datacontext.py

@author: lutianyang5@hivision.com.cn

@version: 0.1
"""
import json
import enum
import locale
from typing import Optional

from sqlalchemy import Column, Integer, String, Text, text, create_engine
from sqlalchemy.orm import sessionmaker, session
from sqlalchemy.ext.declarative import declarative_base

from core.dispatcher import ScriptDispatch, RuleDispatch
from core.fastlogger import getloggerfast
from core.script_engine import IScritEngine
from core.rule_engine import IRuleEngine

logger = getloggerfast(__name__)

Base = declarative_base()
metadata = Base.metadata
LANG_ZONE, CODEPAGE = locale.getdefaultlocale()


class ViewKeyMapper(enum.Enum):
    UnionId = '编号'
    ItemName = '检测项目'
    Level = '等级'
    Advise = '建议'



CheckItemTableHeader = list(map(lambda n: n.value,
                                ViewKeyMapper.__members__.values()))


class CheckItem(Base):
    __tablename__ = 'CheckItem'

    Id = Column(Integer, primary_key=True)
    ItemName = Column(String(50), nullable=False)  # 检查点名字
    UnionId = Column(String(50), name='union_id')
    Description = Column(String(500))
    Advise = Column(Text)  # 修改建议
    Script = Column(Text)
    Script_Engine = Column(String(500))
    Rule = Column(Text, nullable=False)  # 期望值
    Rule_type = Column(String(50), nullable=False) # 期望值的类型
    Rule_Engine = Column(String(500), nullable=False)  # 比较方式
    Exectime = Column(Integer)
    CatogryId = Column(Integer)
    Level = Column(String(50))  # 危险等级
    Enable=Column(Integer)

    _viewkey_mapper = list(ViewKeyMapper.__members__.keys())
    mEnabled = True  # 允许允许
    mPassed = 0  # 检测通过标记
    script_engine = None
    rule_engine = None

    def column(self, col):
        return self.__getattribute__(self._viewkey_mapper[col])

    def setcolumn(self, col, value):
        self.__setattr__(self._viewkey_mapper[col], value)

    def execute_safecheck(self):
        """
        使用内嵌编写的脚本进行检测，颗粒度更加细致
        :return:
        """
        self.script_engine: IScritEngine = ScriptDispatch.load(self.Script_Engine)
        self.rule_engine: IRuleEngine = RuleDispatch.load(self.Rule_Engine)

        self.script_engine.execute(self.Script, self.Exectime)
        hitcnt = self.rule_engine.verify(self.Rule, self.script_engine.stdout.decode(CODEPAGE))
        self.mPassed = 1 if hitcnt > 0 else 0

    def check_scanout_log(self, xmlout, sys_version) -> None:
        """
        使用外部脚本进行扫描的结果进行结果验证
        :param xmlout:外部检测脚本扫描结果
        :return: None
        """
        try:
            if isinstance(xmlout, bytes):
                xmlout = xmlout.decode(CODEPAGE)
            if self.Rule_type == "default":
                rule = self.Rule
            elif self.Rule_type == "custom":
                rule = json.loads(self.Rule)[sys_version]
            else:
                pass
        except Exception as e:
            print (e)
        self.rule_engine: IRuleEngine = RuleDispatch.load(self.Rule_Engine)
        hitcnt = self.rule_engine.verify(rule, xmlout)
        self.mPassed = 1 if hitcnt > 0 else 0


class CheckItemCatgory(Base):
    __tablename__ = 'CheckItemCatgory'

    Id = Column(Integer, primary_key=True)
    CatName = Column(String(50), nullable=False)
    Description = Column(String(500))


class DataController:
    DB_FILE = 'sqlite:///db/SqlSugar.Sqlite3'

    def __init__(self):
        self.dbengine = create_engine(self.DB_FILE)
        self.session_maker = sessionmaker(bind=self.dbengine)
        self.session: Optional[session.Session] = None

    def __enter__(self) -> session.Session:
        self.session = self.session_maker()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            logger.error(exc_val, exc_info=True)

        self.session.close()
        self.session = None

# 数据库字段：
# 1、ID
# 2、比较方式，比较类型
# 3、期望值，列表，字符串数字等
# 4、检查点名字
# 5、危险等级
# 6、修改建议
# 7、检测项类别
