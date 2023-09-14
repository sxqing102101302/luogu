import requests
import re # 用于提取数字
import time
import string
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait # 用于等待网页加载完成
from selenium.webdriver.support import expected_conditions as EC # 用于指定等待网页加载结束的条件
from selenium.webdriver.common.by import By # 用于指定HTML文件中DOM标签元素
import xlwt
options = webdriver.FirefoxOptions() # 设置火狐驱动器的环境
browser = webdriver.Firefox(options=options) # 创建一个火狐驱动器
url = 'https://www.luogu.com.cn/problem/list'
# 用于存字典
data_list = []
# 开始爬取
def start_crawler():
    # 请求url
    browser.get(url)
    # 显示等待输入框是否加载完成
    WebDriverWait(browser, 1000).until(
        EC.presence_of_all_elements_located(
            (  # 洛谷网页源代码里面输入框无ID值，需要从其祖宗元素开始往下定位（从网页源代码处复制即可）
                By.XPATH, "/html/body/div/div[2]/main/div/section/div/section[1]/div[1]/div/div/input")

        )
    )
    for i in ['p', 'sp', 'cf', 'at', 'UVA']:
        search_key = browser.find_element_by_class_name("frame")
        search_key.clear()#清空搜索框后再输入
        search_key.send_keys(i)  # 找到输入框的位置，并输入题目关键字
        browser.find_element_by_xpath(
            "/html/body/div/div[2]/main/div/section/div/section[1]/div[1]/div/button").click()  # 输入关键字后点击搜索
        # 等待题目等信息是否加载完成
        WebDriverWait(browser, 1000).until(
            EC.presence_of_all_elements_located(
                (
                    By.XPATH, "//html/body/div/div[2]/main/div/div/div/div[1]/div[2]")

            )
        )
        # 获取标签信息的条数，确定遍历次数
        divs = browser.find_elements_by_xpath('/html/body/div/div[2]/main/div/div/div/div[1]/div[2]/div')
        # 确定页数
        pages = re.findall(r"\d+", browser.find_element_by_class_name('total').get_attribute('textContent'))
        count = 1
        while (count <= int(pages[0])):
            # 遍历循环
            for div in divs:
                # 获取题号
                numb = div.find_element_by_class_name('pid').text
                # 获取题目
                name = div.find_element_by_class_name('title').text
                # 获取算法（此处需要点击网页中的“显示算法”才能弹出算法
                browser.find_element_by_xpath(
                    "/html/body/div/div[2]/main/div/div/div/div[1]/div[1]/div/div[4]/span/a").click()
                algo = div.find_element_by_class_name('tags-wrap').text
                # 获取来源（此处需要再次点击同样位置的“显示来源”才能弹出来源
                browser.find_element_by_xpath(
                    "/html/body/div/div[2]/main/div/div/div/div[1]/div[1]/div/div[4]/span/a").click()
                sour = div.find_element_by_class_name('tags-wrap').text
                # 获取难度
                diff = div.find_element_by_class_name(
                    'difficulty').text
                # 获取通过率
                rate0 = div.find_element_by_class_name('rate-popup').get_attribute('textContent')
                rate1 = re.findall(r"\d+\.?\d*", div.find_element_by_class_name('rate-popup').get_attribute(
                    'textContent'))  # \d匹配数字\.?匹配小数点\d*匹配小数点后的数字
                sum = 0
                for i in rate0:
                    if i in 'k':
                        sum = sum + 1
                if sum == 0 or sum == 2:
                    rate = "{:.4f}".format(float(rate1[0]) / (0.000001 + float(rate1[1])))
                else:
                    if sum == 1:
                        rate = "{:.4f}".format(float(rate1[0]) / (1000*(0.000001 + float(rate1[1]))))#这里我不知道如何处理分母为0的情况，因为所需数据只保留四位小数，所以就加了一个不会影响数据的数字来除去0值
                # 获取网址
                link = div.find_element_by_class_name(
                    'color-default').get_attribute('href')
                # 获取提交量
                hand1 = rate1[-1]
                if 'k' in rate0:
                    hand = "{:.0f}".format(float(hand1) * 1000)
                else:
                    hand = hand1
                #
                data_dict = {}
                data_dict['numb'] = numb
                data_dict['name'] = name
                data_dict['algo'] = algo
                data_dict['sour'] = sour
                data_dict['diff'] = diff
                data_dict['rate'] = rate
                data_dict['link'] = link
                data_dict['hand'] = hand
                data_list.append(data_dict)
                print(data_dict)
                time.sleep(0.2)  # 停止0.2秒
            browser.find_element_by_xpath('/html/body/div/div[2]/main/div/div/div/div[2]/div/div/div/button[10]').click()
            count = count + 1
    browser.quit()

def main():
    start_crawler()
    # 创建工作簿
    workbook = xlwt.Workbook(encoding = 'utf-8')
    sheet = workbook.add_sheet('资料',cell_overwrite_ok=True)
    head = ['题号', '题目', '算法', '来源', '难度', '通过率', '网址', '提交量']
    for h in range(len(head)):
        # 写入表头
        sheet.write(0, h, head[h])
    j = 1
    for list in data_list:
        k = 0
        for key, data in list.items():
            sheet.write(j, k, data)
            k = k + 1
        j = j + 1
    workbook.save('D:\洛谷.xls')
if __name__ == '__main__':
    main()
