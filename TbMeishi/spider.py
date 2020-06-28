import re
import time

import pymongo
from PIL import Image
from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import *


client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

# browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)

# 设置为开发者模式，防止被识别出来使用了selenium
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-automation'])

browser = webdriver.Chrome(options=options)
wait = WebDriverWait(browser, 10)

# browser.set_window_size(1400, 900)


def isElementPresent(browser,by,value):
    """
    用来判断元素标签是否存在
    """
    try:
        element = browser.find_element(by=by, value=value)
    except Exception as e:
        return False
    else:
        print('存在该元素', element.text)
        return element.text



def login():
    try:
        browser.get('https://login.taobao.com/member/login.jhtml?redirectURL=https%3A%2F%2Fwww.taobao.com%2F')
        submit2 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#login-form > div.login-blocks.sns-login-links > a.weibo-login')))
        submit2.click()
        time.sleep(2)
        input_user = wait.until(EC.presence_of_element_located((By.NAME, 'username')))
        input_pwd = wait.until(EC.presence_of_element_located((By.NAME, 'password')))
        username = input('请输入微博账号:')
        pwd = input('请输入密码:')
        input_user.send_keys(username)
        input_pwd.send_keys(pwd)
        submit3 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#pl_login_logged > div:nth-child(2) > div:nth-child(7) > div:nth-child(1) > a > span')))
        submit3.click()
        time.sleep(3)
        # 判断是否需要验证码登录
        # if isElementPresent(browser, By.XPATH, '//*[@id="pl_login_logged"]/div/div[4]/div/a[1]/img'):
        #     browser.save_screenshot('1.img')
            
        #     img = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="pl_login_logged"]/div/div[4]/div/a[1]/img')))
        #     time.sleep(2)
        #     location = img.location
        #     print(location)
        #     size = img.size
        #     print(size)
        #     left = location['x'] + size['width']
        #     top = location['y'] + size['height']
        #     right = left + size['width'] + size['width'] + 40
        #     bottom = top + size['height'] + size['height']
        #     print(right, bottom)
        #     page = Image.open('1.png')
        #     image_obj = page.crop((left, top, right, bottom))
        #     image_obj.show()
        #     code = input('请输入验证码:')
        #     input_code = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'pl_login_logged > div > div:nth-child(4) > div > input')))
        #     input_code.send_keys(code)
        #     submit3 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#pl_login_logged > div > div:nth-child(7) > div:nth-child(1) > a')))
        #     submit3.click()
        #     time.sleep(2)
        return browser
    except Exception as e:
        print(e)
        # login()



def search():
    print('正在搜索')
    try:
        browser.get('https://www.taobao.com')
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#q"))
        )
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#J_TSearchForm > div.search-button > button")))
        input.send_keys(KEYWORD)
        submit.click()
        time.sleep(7)
        total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total')))
        get_products()
        return total.text
    except TimeoutException:
        return search()
        

def next_page(page_number):
    print('正在翻页', page_number)
    try:
        input = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > input"))
            )
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit")))
        input.clear()
        input.send_keys(page_number)
        submit.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'), str(page_number)))
        get_products()
    except TimeoutException:
        next_page(page_number)

def get_products():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'image': item.find('.pic .img').attr('src'), 
            'price': item.find('.price').text(), 
            'deal': item.find('.deal-cnt').text()[:-3], 
            'title': item.find('.title').text(), 
            'shop': item.find('.shop').text(), 
            'location': item.find('.location').text()
        }
        print(product)
        save_to_mongo(product)

def save_to_mongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print('存储到MONGODB成功', result)
    except Exception as e:
        print('存储到MONGODB失败', e, result)


def main():
    try:
        login()
        total = search()
        total = int(re.compile('(\d+)').search(total).group(1))
        print(total)
        for i in range(2, total+1):
            next_page(i)
    except Exception as e:
        print('出错了')
        print(e)
    finally:
        browser.close()

if __name__ == "__main__":
    main()
