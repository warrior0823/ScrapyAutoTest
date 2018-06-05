# -*- coding: utf-8 -*-


import MySQLdb.cursors
from selenium import webdriver
from time import sleep
import time
import re
import unittest


class test_mkls_scrapy(unittest.TestCase):

    '''
    麦康莱斯
    '''

    def test_mkls(self):
        # 线上环境
        # db = MySQLdb.connect(host='573ed969b9aa4.bj.cdb.myqcloud.com',
        #                      port=5295,
        #                      user='cdb_outermaller',
        #                      passwd='wmqe20151118',
        #                      cursorclass=MySQLdb.cursors.DictCursor)

        # 测试环境
        db = MySQLdb.connect(host='db1.dev1.yiyao.cc',
                             port=13306,
                             user='mall_root',
                             passwd='20151118',
                             cursorclass=MySQLdb.cursors.DictCursor,
                             charset='utf8')
        cursor = db.cursor()

        # 麦斯康莱查询
        sql = 'SELECT c.item_out_id AS "ID", c.accept_sn AS "国药准字", c.item_name AS "商品名字", c.factory_name AS "生产厂家", c.sale_price AS "零售价", p.single_price AS "显示价格", c.pkg_name AS "规格名称", c.unit_name AS "单位", c.item_category AS "分类/剂型", c.has_inventory AS "has_inventory", c.inventory_desc AS "库存", c.is_health_care AS "医保类型", c.item_insurance_price AS "维护价格", c.item_site_insurance_price AS "医保价格", c.item_promotion AS "促销信息", c.item_promotion_url AS "促销url", c.otc_type AS "OTC分类", c.is_rx AS "是否rx", c.`status` AS "状态", c.middle_quantity AS "中包", c.big_quantity AS "大包", p.middle_price AS "中包价格", p.big_price AS "大包价格", c.image_status AS "图片", c.item_instructions AS "说明书", c.item_instructions_ori_url AS "说明书图片", c.item_detail_url AS "详情地址", c.modify_time AS "爬取时间" FROM mall_crawl.crawl_item_scrapy c, mall_crawl.crawl_item_price p WHERE c.company_sid = 10000 AND c.sid = p.item_sid and c.modify_time > "%s" AND c.item_name LIKE "%%双黄连口服液%%";' % time.strftime("%Y-%m-%d")

        cursor.execute(sql)
        data1 = cursor.fetchall()
        data = list(data1)

        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        driver = webdriver.Chrome(chrome_options=option)
        # 登陆
        driver.get("http://www.br511.com/MenberCenter/Login.aspx")
        sleep(2)
        driver.find_element_by_id("txtLoginId").send_keys("21011085")
        sleep(2)
        driver.find_element_by_id("txtPassword").send_keys("090907")
        driver.find_element_by_id("btnLogin").click()
        sleep(2)
        driver.find_element_by_id("top1_txtKeyword").send_keys(u"双黄连口服液")
        driver.find_element_by_id("top1_btnSearch").click()
        sleep(2)
        meds = driver.find_elements_by_class_name("products_td")

        '''
        判断1：数据库搜索结果与页面查询结果是否一致
        '''
        if len(meds) == len(data):
            print len(meds)
        else:
            raise "数据库搜索结果与页面查询结果不一致！"

        # 对浏览器进行操作
        # 从第一个搜索结果开始进入商品详情页面
        try:
            for i in range(len(meds)):
                driver.find_element_by_xpath(
                    '//*[@id="form1"]/div[3]/div[3]/div[6]/div[1]/table/tbody/tr[%s]/td[1]/a[1]/img' % int(i+2)).click()
                sleep(2)
                all_handles = driver.window_handles
                curr_window = driver.current_window_handle
                for k in all_handles:
                    if k != curr_window:
                        driver.switch_to.window(k)
                url = driver.current_url
                pattern = re.compile(r'PID=(.*?)&')
                result = re.search(pattern, url)
                res_cut = result.group()

                # 页面url，数据库中的item_out_id，也是数据库第一列值
                id_page = res_cut.split("=")[1].split("&")[0]

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
                sale_price_page = driver.find_element_by_id("lblPrice_Cash").text
                print "sale_price_page", sale_price_page
                print "sale_price", sale_price
                assert sale_price == float(sale_price_page)

                # 生产厂家 = factory_name
                factory_name_page = driver.find_element_by_id("lblFromPlace").text
                print type(factory_name_page)
                assert factory_name == factory_name_page

                # 国药准字=accept_sn
                accept_sn_page = driver.find_element_by_id("lblAlias_Name").text
                # print accept_sn_page
                # print accept_sn
                assert accept_sn == accept_sn_page

                # 商品名字=item_name
                item_name_page = driver.find_element_by_id("lblPNameModel").text
                # print item_name_page
                # print item_name
                assert item_name == item_name_page

                # 单位=unit_name
                unit_name_page = driver.find_element_by_id("lblBaseUnit").text
                # print unit_name_page
                # print unit_name
                assert unit_name == unit_name_page

                # 库存=inventory_desc
                inventory_desc_page = driver.find_element_by_id("lblQuantitys").text
                # print inventory_desc_page
                # print inventory_desc
                assert inventory_desc == inventory_desc_page.replace(' ', '')

                # 医保类型
                is_health_care_page = driver.find_element_by_id("lblPTypeH").text
                if is_health_care_page == '':
                    assert is_health_care == None
                elif is_health_care_page == u'甲类':
                    assert is_health_care == 5
                elif is_health_care_page == u'乙类':
                    assert is_health_care == 6
                elif is_health_care_page == u'丙类':
                    assert is_health_care == 7

                # 中包
                middle_quantity_page = driver.find_element_by_id("lblMiddleCount").text
                # print middle_quantity_page
                # print middle_quantity
                assert middle_quantity == float(middle_quantity_page)

                # 大包
                big_quantity_page = driver.find_element_by_id("lblLargeCount").text
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
