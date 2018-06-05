# -*- coding: utf-8 -*-


import MySQLdb.cursors
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import time
import re
import unittest


class test_zy_scrapy(unittest.TestCase):

    '''
    震元
    '''

    def test_zy(self):
        # 线上环境
        # db = MySQLdb.connect(host='',
        #                      port=1,
        #                      user='',
        #                      passwd='',
        #                      cursorclass=MySQLdb.cursors.DictCursor)

        # 测试环境
        db = MySQLdb.connect(host='',
                             port=1,
                             user='',
                             passwd='',
                             cursorclass=MySQLdb.cursors.DictCursor,
                             charset='utf8')
        cursor = db.cursor()

        # 麦斯康莱查询
        sql = 'SELECT c.item_out_id AS "ID", c.accept_sn AS "国药准字", c.item_name AS "商品名字", c.factory_name AS "生产厂家", c.sale_price AS "零售价", p.single_price AS "显示价格", c.pkg_name AS "规格名称", c.unit_name AS "单位", c.item_category AS "分类/剂型", c.has_inventory AS "has_inventory", c.inventory_desc AS "库存", c.is_health_care AS "医保类型", c.item_insurance_price AS "维护价格", c.item_site_insurance_price AS "医保价格", c.item_promotion AS "促销信息", c.item_promotion_url AS "促销url", c.otc_type AS "OTC分类", c.is_rx AS "是否rx", c.`status` AS "状态", c.middle_quantity AS "中包", c.big_quantity AS "大包", p.middle_price AS "中包价格", p.big_price AS "大包价格", c.image_status AS "图片", c.item_instructions AS "说明书", c.item_instructions_ori_url AS "说明书图片", c.item_detail_url AS "详情地址", c.modify_time AS "爬取时间" FROM mall_crawl.crawl_item_scrapy c, mall_crawl.crawl_item_price p WHERE c.company_sid = 10006 AND c.sid = p.item_sid and c.modify_time > "%s" AND c.item_name LIKE "%%感冒清热颗粒%%";' % time.strftime("%Y-%m-%d")

        cursor.execute(sql)
        data1 = cursor.fetchall()
        data = list(data1)

        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        driver = webdriver.Chrome(chrome_options=option)
        # 登陆
        driver.get("http:///login.jsp")
        sleep(2)
        driver.find_element_by_id("loginName").send_keys("")
        sleep(2)
        driver.find_element_by_id("loginPwd").send_keys("")
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
            z = len(s) + len(y)
        except:
            # s = driver.find_elements_by_class_name("price_listbox_background price_listbox")
            s = driver.find_elements_by_class_name("price_listbox")
            z = len(s)

        '''
        判断1：数据库搜索结果与页面查询结果是否一致
        '''
        if z == len(data):
            print z
        else:
            raise "数据库搜索结果与页面查询结果不一致！"

        # 对浏览器进行操作
        # 从第一个搜索结果开始进入商品详情页面
        try:
            for i in range(z):
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
                url = driver.current_url
                # 匹配页面url的id
                pattern = re.compile(r'\d*$')
                result = re.search(pattern, url)
                id_page = result.group()

                for j in range(len(data)):
                    id_url = data[j]['ID']

                    if id_page == id_url:
                        print id_url
                        print data[j]['ID']
                        print '*' * 40
                        accept_sn = data[j]['国药准字']
                        print accept_sn
                        item_name = data[j]['商品名字']
                        print item_name
                        factory_name = data[j]['生产厂家']
                        print factory_name
                        sale_price = data[j]['显示价格']
                        print sale_price
                        unit_name = data[j]['单位']
                        print unit_name
                        print data[j]['规格名称']
                        print data[j]['has_inventory']
                        inventory_desc = data[j]['库存']
                        print inventory_desc
                        is_health_care = data[j]['医保类型']
                        print is_health_care
                        middle_quantity = data[j]['中包']
                        print middle_quantity
                        big_quantity = data[j]['大包']
                        print big_quantity
                        image_status = data[j]['图片']
                        print image_status
                        print '*' * 40
                # 页面
                # 现价=sale_price
                sale_price_page = driver.find_element_by_xpath("html/body/div[3]/div/div[2]/dl/dd/i").text
                sale_price_page = sale_price_page.split(' ')[0].encode('utf-8').split('￥')[1]
                assert sale_price == float(sale_price_page)

                # 生产厂家 = factory_name
                factory_name_page = driver.find_element_by_xpath("html/body/div[3]/div/div[2]/dl/i/dd[3]").text
                factory_name_page = factory_name_page[3:]
                assert factory_name == factory_name_page

                # 国药准字=accept_sn
                accept_sn_page = driver.find_element_by_xpath("html/body/div[3]/i/div[2]/div[2]/div[1]/dl/dd[11]").text
                accept_sn_page = accept_sn_page[5:]
                assert accept_sn == accept_sn_page

                # 商品名字=item_name
                item_name_page = driver.find_element_by_xpath("html/body/div[3]/div/div[2]/h3").text
                # item_name_page = item_name_page.split('/')[0]
                assert item_name == item_name_page

                # 单位=unit_name
                unit_name_page = driver.find_element_by_xpath("html/body/div[3]/i/div[2]/div[2]/div[1]/dl/dd[5]").text
                unit_name_page = unit_name_page.split(':')[1]
                assert unit_name == unit_name_page

                # 库存=inventory_desc
                inventory_desc_page = driver.find_element_by_xpath(".//*[@id='pro_count']/span").text
                patt = re.compile(r'\(.*?\)')
                res = patt.search(inventory_desc_page)
                inventory_desc_page = res.group().replace(' ', '').replace('(', '').replace(')', '')
                assert inventory_desc == inventory_desc_page

                # 医保类型
                is_health_care_page = driver.find_element_by_xpath("html/body/div[3]/i/div[2]/div[2]/div[1]/dl/dd[4]").text
                is_health_care_page = is_health_care_page.split(':')[1]
                if is_health_care_page == '':
                    assert is_health_care == None
                elif is_health_care_page == u'甲类':
                    assert is_health_care == 5
                elif is_health_care_page == u'乙类':
                    assert is_health_care == 6
                elif is_health_care_page == u'丙类':
                    assert is_health_care == 7

                # 中包
                middle_quantity_page = driver.find_element_by_xpath("html/body/div[3]/i/div[2]/div[2]/div[1]/dl/dd[8]").text
                middle_quantity_page = middle_quantity_page.split(':')[1].split('\\')[0].split(' ')[0]
                assert middle_quantity == float(middle_quantity_page)

                # 大包
                big_quantity_page = driver.find_element_by_xpath("html/body/div[3]/i/div[2]/div[2]/div[1]/dl/dd[8]").text
                big_quantity_page = big_quantity_page.split(':')[1].split('\\')[1].split(' ')[1]
                # print big_quantity_page
                # print big_quantity
                assert big_quantity == float(big_quantity_page)
                # 关闭新打开的页面
                driver.close()
                # 回到搜索结果页
                driver.switch_to.window(curr_window)
        finally:
            # 关闭数据库连接
            db.close()
