# -*- coding: utf-8 -*-
# @Time     : 2021/6/8 下午7:42
# @Author   : binger

import os

ROOT = os.curdir


def build_app(name, project=None):
    path = os.path.join(project or ROOT, "app", name)
    os.mkdir(path)
    str_blue_print = f"""
# -*- coding: utf-8 -*-

from flask import Blueprint

from {project or ".."}.metrics.extensions import register_blueprint

api = Blueprint(__name__.split(".")[-1], __name__)
register_blueprint(api, url_prefix='/common')

from . import views

    """
    with open(os.path.join(path, "__init__.py"), "w") as fw:
        fw.write(str_blue_print)

    str_views = """
# -*- coding: utf-8 -*-
from . import api

    """
    with open(os.path.join(path, "views.py"), "w") as fw:
        fw.write(str_views)

    print(f"create app: {name}, include: __init__.py, views.py")

    if project:
        with open(os.path.join(project, "app", "auto_load.py"), mode="w+") as fw:
            fw.write(f"from . import {name}{os.linesep}")
        print(f"add {name} to blueprint")


def build_project(name, path=None):
    # 创建项目目录
    from .setting import ROOT_PATH
    path = os.path.join(path or ROOT, name)
    os.mkdir(path)
    # # 通过解压缩 生成项目主体
    project_zip_path = os.path.join(ROOT_PATH, "conf", "project.zip")
    import zipfile

    with zipfile.ZipFile(project_zip_path) as zf:
        zf.extractall(path)

    # 文件迁移
    from shutil import copyfile
    file_requirements = os.path.join(path, "requirements.txt")
    copyfile(os.path.join(ROOT_PATH, "conf", "requirements.txt"), file_requirements)
    print(f"add requirements.txt: {file_requirements}")
    manager = """
# -*- coding: utf-8 -*-

from {name}.cli import manager

if __name__ == '__main__':
    manager()
    """
    file_manager = os.path.join(path, "manager.py")
    with open(file_manager, "w") as fw:
        fw.write(manager.format(name=name))
    print("build project over")
    # 拷贝配置文件和目录
