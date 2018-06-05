# coding: utf-8

import unittest


def testcaseDir(test_directory):

    discover = unittest.defaultTestLoader.discover(test_directory, pattern='test*.py', top_level_dir=test_directory)
    return discover
