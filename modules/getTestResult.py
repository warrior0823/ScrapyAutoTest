# coding: utf-8

from selenium import webdriver
from time import sleep


def get_results(filename):
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=option)
    driver.maximize_window()
    result_url = "file://%s" % filename
    driver.get(result_url)
    sleep(3)
    res = driver.find_element_by_xpath("/html/body/div[1]/p[4]").text
    result = res.split(':')
    driver.quit()
    return result[-1]
