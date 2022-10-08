# -*- coding: utf-8 -*-
# @Time     : 2021/6/8 下午7:42
# @Author   : binger

import os
import zipfile
from flask_os.setting import ROOT_PATH


def build_project_zip(path="project", dst_zip_file=None):
    dst_filename = dst_zip_file or os.path.join(ROOT_PATH, "conf", "project.zip")
    with zipfile.ZipFile(dst_filename, "w", zipfile.ZIP_DEFLATED) as fw:

        for parent, dirnames, filenames in os.walk(path):
            dst_parent = parent.replace(path, "")
            for filename in filenames:
                if filename.startswith("."):
                    continue
                src_file = os.path.join(parent, filename)
                dst_name = os.path.join(dst_parent, filename)
                fw.write(src_file, dst_name)


build_project_zip()