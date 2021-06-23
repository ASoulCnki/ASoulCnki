# -*- encoding: utf-8 -*-
"""
Filename         :setup.py
Description      :使用Cython编译查重代码加速
Time             :2021/06/23 08:38:56
Author           :hwa
Version          :1.0
"""

# python setup.py build_ext --inplace
from distutils.core import setup
from Cython.Build import cythonize

setup(name='check',
      ext_modules=cythonize("check.py"))
