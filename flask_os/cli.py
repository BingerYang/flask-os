# -*- coding: utf-8 -*-
# @Time     : 2021/6/11 上午10:48
# @Author   : binger
import argparse

parser = argparse.ArgumentParser(prog='flask_cli')
subparsers = parser.add_subparsers(help='sub-command help')


def run_project(args):
    from flask_os import build_project
    build_project(name=args.name, path=None)


def run_app(args):
    from flask_os import build_app
    build_app(name=args.name, project=args.project)


parser_project = subparsers.add_parser('project', help='flask os create')
parser_project.add_argument('name', type=str, help='新建flask项目名字')
parser_project.add_argument('--path', "-P", type=str, help='新建项目路径，默认：当前目录')
parser_project.set_defaults(func=run_project)

parser_app = subparsers.add_parser('app', help='flask app create')
parser_app.add_argument('name', type=str, help='新建flask app 名字')
parser_app.add_argument('--project', type=str, help='归属项目名称，必须存在')
parser_app.set_defaults(func=run_app)

args = parser.parse_args()
args.func(args)
import sys

sys.exit(0)
