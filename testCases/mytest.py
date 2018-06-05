# coding: utf-8

import time
import re
from time import sleep
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("")
sleep(2)
driver.find_element_by_id("loginName").send_keys("")
sleep(2)
driver.find_element_by_id("loginPwd").send_keys("11")
driver.find_element_by_id("ptLogin").click()
sleep(3)
alert_window = EC.alert_is_present()(driver)
if alert_window:
    print alert_window.text
    alert_window.accept()
sleep(2)
driver.find_element_by_id("searchTitle").click()
driver.find_element_by_id("searchTitle").send_keys(u"感冒清热颗粒")
driver.find_element_by_xpath(".//*[@id='searchForm']/div/input[2]").click()
sleep(3)
try:
    s = driver.find_elements_by_class_name("price_listbox")
    y = driver.find_elements_by_class_name("price_listbox2")
    z = len(s)+len(y)
except:
    # s = driver.find_elements_by_class_name("price_listbox_background price_listbox")
    s = driver.find_elements_by_class_name("price_listbox")
    z = len(s)

try:
    for i in range(z):
        print i
        try:
            driver.find_element_by_xpath(
                'html/body/div[2]/div[4]/div/div[1]/div[3]/div[%s]/span[1]/a[2]' % int(i + 2)).click()
        except:
            driver.find_element_by_xpath(
                'html/body/div[2]/div[4]/div/div[1]/div[3]/div[%s]/span[1]/a' % int(i + 2)).click()
        all_handles = driver.window_handles
        curr_window = driver.current_window_handle
        for k in all_handles:
            if k != curr_window:
                driver.switch_to.window(k)
        sleep(2)
        #价格
        sale_price_page = driver.find_element_by_xpath("html/body/div[3]/div/div[2]/dl/dd/i").text
        sale_price_page = sale_price_page.split(' ')[0].encode('utf-8').split('￥')[1]
        print type(float(sale_price_page))
        print float(sale_price_page)
        # 生产厂家
        factory_name_page = driver.find_element_by_xpath("html/body/div[3]/div/div[2]/dl/i/dd[3]").text
        factory_name_page = factory_name_page[3:]
        print type(factory_name_page)
        print factory_name_page
        # 国药准字=accept_sn
        accept_sn_page = driver.find_element_by_xpath("html/body/div[3]/i/div[2]/div[2]/div[1]/dl/dd[11]").text
        accept_sn_page = accept_sn_page[5:]
        print type(accept_sn_page)
        print accept_sn_page
        # 商品名字=item_name
        item_name_page = driver.find_element_by_xpath("html/body/div[3]/div/div[2]/h3").text
        print type(item_name_page.split('/')[0])
        print item_name_page
        # 单位=unit_name
        unit_name_page = driver.find_element_by_xpath("html/body/div[3]/i/div[2]/div[2]/div[1]/dl/dd[5]").text
        print type(unit_name_page.split(':')[1])
        # 库存=inventory_desc
        inventory_desc_page = driver.find_element_by_xpath(".//*[@id='pro_count']/span").text
        patt = re.compile(r'\(.*?\)')
        res = patt.search(inventory_desc_page)
        inventory_desc_page = res.group().replace(' ', '').replace('(', '').replace(')', '')
        print type(inventory_desc_page)
        # 医保类型
        is_health_care_page = driver.find_element_by_xpath("html/body/div[3]/i/div[2]/div[2]/div[1]/dl/dd[4]").text
        print is_health_care_page.split(':')[1]
        # 中包
        middle_quantity_page = driver.find_element_by_xpath("html/body/div[3]/i/div[2]/div[2]/div[1]/dl/dd[8]").text
        middle_quantity_page = middle_quantity_page.split(':')[1].split('\\')[0].split(' ')[0]
        print type(middle_quantity_page)
        # 大包
        big_quantity_page = driver.find_element_by_xpath("html/body/div[3]/i/div[2]/div[2]/div[1]/dl/dd[8]").text
        print big_quantity_page
        big_quantity_page = big_quantity_page.split(':')[1].split('\\')[0].split(' ')[2]
        print type(big_quantity_page)
        print "big_quantity_page", big_quantity_page
        driver.close()
        driver.switch_to.window(curr_window)
finally:
    pass
