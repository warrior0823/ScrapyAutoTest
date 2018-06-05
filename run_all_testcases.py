# coding: utf-8

import time
from modules import *
from testCases import dir_path
from test_reports import testReport_path
from HTMLTestRunner import HTMLTestRunner


if __name__ == '__main__':

    # 测试用例路径
    test_dir = dir_path.dir_path()
    # 测试报告存放路径
    report_dir = testReport_path.report_path()

    currTime = time.strftime('%Y-%m-%d')
    filename = report_dir + '\\report' + currTime + '.html'
    fp = open(filename, 'wb')
    runner = HTMLTestRunner(stream=fp, title='爬虫数据自动化测试', description='用例执行结果')
    runner.run(getTestcases.testcaseDir(test_dir))
    fp.close()
    result = getTestResult.get_results(filename)
    mail = sendEmail.send_Mail(filename, result)
    if mail:
        print u'邮件发送成功！'
    else:
        print u'邮件发送失败！'
