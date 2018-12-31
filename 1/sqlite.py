#导入webdriver
from selenium import webdriver
import time
import sqlite3
import re
from selenium.webdriver.common.action_chains import ActionChains

#连接到数据库
connect = sqlite3.connect("zhubo.sqlite3")
# 创建了一个游标对象：cursor
cursor = connect.cursor()

chromeOptions = webdriver.ChromeOptions()

browser = webdriver.Chrome()
browser.maximize_window()
browser.get("https://www.douyu.com/633019")

# 3秒等待网页加载完成
time.sleep(3)

# 点击登录按钮
log = browser.find_element_by_xpath('//*[@id="js-header"]/div/div/div[4]/div[6]/div/a[1]')
log.click()
time.sleep(4)#等待四秒加载弹出框

browser.switch_to_frame("login-passport-frame")#切换到登录弹出的iframe并点击实现用户登录
browser.find_element_by_xpath('//*[@id="js-authorized-box"]/div[2]/div[1]/img').click()
# 等待5秒，网页重新载入
time.sleep(5)

# 点击切换到贵族列表
noble_list = browser.find_element_by_xpath("//*[@id='js-player-asideMain']/div/div[1]/div[2]/div/div/div/div[1]/ul/li[2]/div")
noble_list.click()


noble_3 = []# 获取贵族列表，包含3个贵族
noble_3 = browser.find_elements_by_class_name("NobleRankList-item--top")

href_3= ["","",""]#存储三个贵族的鱼吧主页链接
index  = 0

# 分别打印三个贵族的信息
for person in noble_3:

    icon = person.find_element_by_class_name('NobleRankList-pic')
    icon.click()

    time.sleep(1)
    name = icon.find_element_by_xpath('//*[@id="js-player-asideMain"]/div/div[3]/div/div/div[1]/div/div[2]/div[3]/a')
    print(name.text)#打印贵族的昵称
    names = name.text

    noble = icon.find_element_by_xpath('//*[@id="js-player-asideMain"]/div/div[1]/div[2]/div/div/div/div[2]/div[2]/div/div[2]/div[1]/ul/li[1]/img')
    print(noble.get_attribute('title'))#打印贵族的级别（骑士、公爵...）
    nobles = noble.get_attribute('title')

    user_level = icon.find_element_by_xpath('//*[@id="js-player-asideMain"]/div/div[3]/div/div/div[1]/div/div[2]/div[3]/div/span')
    print(user_level.get_attribute('title'))#打印贵族的等级
    user_levels = user_level.get_attribute('title')

    user_head =  icon.find_element_by_xpath('//*[@id="js-player-asideMain"]/div/div[3]/div/div/div[1]/div/div[2]/a')
    print(user_head.get_attribute('href'))#打印贵族的鱼吧主页链接
    user_heads = user_head.get_attribute('href')

    href_3[index]= user_head.get_attribute('href')
    index = index + 1

    user_image = user_head.find_element_by_class_name('NobleCard-icon')
    print(user_image.get_attribute('src'))#打印贵族的头像链接地址
    user_images = user_image.get_attribute('src')
    time.sleep(1)

    # # id, names, rank, guanzhu, fensi, jianjie, touxiang, zhuye, roomid)
    # sql = 'insert into guizu values(?,?,?,?,?,?,?,?,?)'
    # for t in [(id,names,user_levels,user_levels,user_levels,user_levels,user_images,user_heads,633019)]:
    #     connect.execute(, t)
# print(href_3)

index =0
for yuba in range(len(noble_3)):
    browser.get(href_3[yuba])
    time.sleep(2)
    num = browser.find_elements_by_class_name('index-HeaderCount-hQ86V')

    print(num[0].text)#打印关注数
    print(num[1].text)#打印粉丝数
    sex = browser.find_element_by_xpath('//*[@id="fixedScroll"]/div[1]/div[2]/div[2]')
    print(sex.text[2])#打印性别

    intro = browser.find_element_by_xpath('//*[@id="fixedScroll"]/div[1]/div[2]/div[3]/p')
    print(intro.text)#打印简介
    time.sleep(1)

# 关闭游标
cursor.close()
# 关闭数据库
connect.close()


