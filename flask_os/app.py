# -*- coding: utf-8 -*-
# @Time     : 2021/6/8 下午7:42
# @Author   : binger

import os

ROOT = os.curdir


def build_app(name, project=None):
    project_root = os.path.abspath(ROOT)
    project = os.path.abspath(project or os.path.join(project_root, os.path.basename(project_root)))
    path = os.path.join(project, "app", name)
    os.mkdir(path)
    str_blue_print = f"""
# -*- coding: utf-8 -*-

from flask import Blueprint

from ...metrics import register_blueprint

api = Blueprint(__name__.split(".")[-1], __name__)
register_blueprint(api, url_prefix='/{name}')

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
        with open(os.path.join(project, "app", "auto_load.py"), mode="a+") as fw:
            fw.write(f"from . import {name}{os.linesep}")
        print(f"add {name} to blueprint")


def build_project(name, path=None):
    # 创建项目目录
    from .setting import ROOT_PATH
    path = path or ROOT
    os.makedirs(path, exist_ok=True)
    # 通过解压缩 生成项目主体
    project_zip_path = os.path.join(ROOT_PATH, "conf", "project.zip")
    import zipfile, shutil

    from tempfile import TemporaryDirectory
    with TemporaryDirectory() as dirname:
        _path = os.path.join(dirname, name)
        with zipfile.ZipFile(project_zip_path) as zf:
            zf.extractall(_path)
        shutil.move(_path, path)

    # 是否改变tpl的位置
    shutil.move(os.path.join(path, name, "etc"), os.path.join(path, "etc"))

    # 文件迁移
    from shutil import copyfile
    file_requirements = os.path.join(path, "requirements.txt")
    copyfile(os.path.join(ROOT_PATH, "conf", "requirements.txt"), file_requirements)
    print(f"add requirements.txt: {file_requirements}")
    manager = f"""
# -*- coding: utf-8 -*-

from {name}.cli import manager

if __name__ == '__main__':
    manager()
    """
    file_manager = os.path.join(path, "manager.py")
    with open(file_manager, "w") as fw:
        fw.write(manager)
    print(f"add manager.py: {file_manager}")

    wsgi_file_tpl = f"""
from gevent import monkey

monkey.patch_all()

from {name}.app import create_app

app = create_app()    
"""
    file_wsgi = os.path.join(path, name, "wsgi.py")
    with open(file_wsgi, "w") as fw:
        fw.write(wsgi_file_tpl)
    print(f"add wsgi.py: {file_wsgi}")

    print("build project over")
    # 拷贝配置文件和目录