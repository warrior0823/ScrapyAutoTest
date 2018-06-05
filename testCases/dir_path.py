# coding: utf-8

import os


# 获取当前文件夹路径
def dir_path():
    return os.path.split(os.path.realpath(__file__))[0]
