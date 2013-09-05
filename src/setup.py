# -*- coding:utf-8 -*-
"""
Created on 5 mar 2010

@author: Filip
"""
from distutils.core import setup
import py2exe

setup(windows=['picomotor_mcl.py'], options = { "py2exe":{"dll_excludes":["MSVCP90.dll"]}})