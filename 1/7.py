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

rooms = []#存储房间列表
sql = '''select room_id from roomtable order by hot desc'''
cursor.execute(sql)    #该例程执行一个 SQL 语句
rooms=cursor.fetchall()      #该例程获取查询结果集中所有（剩余）的行，返回一个列表
print(rooms)
room_s =[]
for r in rooms:
    r = str(r).split("('")[1]
    r = r.split("',")[0]
    print(r)
    room_s.append(r)
flag = 0
for room_id in room_s :

    browser.get("https://www.douyu.com/" + room_id)

    # 3秒等待网页加载完成
    time.sleep(3)
    if flag ==0 :
        # 点击登录按钮
        log = browser.find_element_by_xpath('//*[@id="js-header"]/div/div/div[4]/div[6]/div/a[1]')
        log.click()
        time.sleep(4)#等待四秒加载弹出框

        browser.switch_to_frame("login-passport-frame")#切换到登录弹出的iframe并点击实现用户登录
        browser.find_element_by_xpath('//*[@id="js-authorized-box"]/div[2]/div[1]/img').click()
        # 等待5秒，网页重新载入
        time.sleep(5)
        flag=1

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
        user_levels = str(user_levels).split('：')[1]

        user_head =  icon.find_element_by_xpath('//*[@id="js-player-asideMain"]/div/div[3]/div/div/div[1]/div/div[2]/a')
        print(user_head.get_attribute('href'))#打印贵族的鱼吧主页链接
        user_heads = user_head.get_attribute('href')

        id = str(user_heads).split('id=')[1]
        print('鱼吧id：' + id)

        href_3[index]= user_head.get_attribute('href')
        index = index + 1

        user_image = user_head.find_element_by_class_name('NobleCard-icon')
        print(user_image.get_attribute('src'))#打印贵族的头像链接地址
        user_images = user_image.get_attribute('src')
        time.sleep(1)

        # # id, names, rank, guanzhu, fensi, jianjie, touxiang, zhuye, roomid)
        # 构造sql语句
        sql = '''insert into guizu values(?,?,?,?,?,?,?,?,?,?)'''
        # 执行sql语句
        for t in [(id,names,user_levels,0,0,0,user_images,user_heads,room_id,'女')]:
            cursor.execute(sql,t)
        connect.commit()

    index =0
    for yuba in range(len(noble_3)):
        browser.get(href_3[yuba])
        time.sleep(2)
        num = browser.find_elements_by_class_name('index-HeaderCount-hQ86V')

        id = str(href_3[index]).split('id=')[1]
        print('鱼吧id：' + id)
        index = index + 1

        print(num[0].text)#打印关注数
        print(num[1].text)#打印粉丝数
        sex = browser.find_element_by_xpath('//*[@id="fixedScroll"]/div[1]/div[2]/div[2]')
        sexs = sex.text[2]
        if ((sexs != '男') & (sexs != '女')):
            sexs = '未知'

        print(sexs)#打印性别

        intro = browser.find_element_by_xpath('//*[@id="fixedScroll"]/div[1]/div[2]/div[3]/p')
        print(intro.text)#打印简介


        # # id, names, rank, guanzhu, fensi, jianjie, touxiang, zhuye, roomid)
        # 构造sql语句
        sql = '''update guizu set (guanzhu,fensi,sex,jianjie) = (?,?,?,?) where id = ?'''
        # 执行sql语句
        for t in [(num[0].text,num[1].text,sexs,intro.text,id)]:
            cursor.execute(sql, t)
        connect.commit()
        time.sleep(1)

# 关闭游标
cursor.close()
# 关闭数据库
connect.close()


