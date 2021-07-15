# -*- coding: utf-8 -*-
# @Time     : 2021/6/7 上午11:23
# @Author   : binger
name = __package__
version_info = (0, 1, 21071519)
__version__ = ".".join([str(v) for v in version_info])
__description__ = 'flask项目基础一键生成'

from .app import build_project, build_app
