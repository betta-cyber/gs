#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()


# 定义User对象:
class Task(Base):
    # 表的名字:
    __tablename__ = 'tasks'

    # 表的结构:
    rowid = Column(Integer())
    task_id = Column(String(64), primary_key=True)
    ip = Column(String(64))
    port = Column(String(64))
    os = Column(String(64))
    username = Column(String(255))
    password = Column(String(255))
    status = Column(String(255))
    update_time = Column(DateTime())
    op_user = Column(String(255))


engine = create_engine('sqlite:///gcheck.db3')
DBSession = sessionmaker(bind=engine)