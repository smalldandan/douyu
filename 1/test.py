import requests
import json
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
from fontTools.ttLib import TTFont
from selenium import webdriver
import time
import sqlite3
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import  xml.dom.minidom

urls = ['https://www.douyu.com/gapi/rkc/directory/2_2/{}'.format(page) for page in range(1, 2)]
detail_url = 'https://www.douyu.com/betard/'
room_url = 'https://www.douyu.com/'

def getHtmlurl(url):         #获取网址
    try:
       r=requests.get(url)
       r.raise_for_status()
       r.encoding='utf-8'
       return r.text
    except:
        return ""

#连接到数据库
connect = sqlite3.connect("zhubo.sqlite3")
# 创建了一个游标对象：cursor
cursor = connect.cursor()


chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument('headless')

driver = webdriver.Chrome()#options=chromeOptions
driver.maximize_window()

for url in urls:
    res = requests.get(url)
    j = json.loads(res.text)
    data = j['data']  # 通过观察可以发现要的数据在data下
    data_rl = data['rl']  # 在观察发现在data的rl中

    print('主播 房间号 房间名 热度')

    for i in range(len(data_rl)):  # 这里用到for循环来处理一个列表下多个字典的数据
        # if i > 5 :
        #     break
        Anchor = str(data_rl[i]['nn']) # 获取主播名字
        RoomNumber = str(data_rl[i]['rid'])  # 获取房间号
        if ((RoomNumber==525207) | (RoomNumber==6192150)|(RoomNumber==3919268)):
            continue
        Heat = int(data_rl[i]['ol'])  # 获取热度
        RoomName = str(data_rl[i]['rn'])  # 获取房间名
        print(Anchor, RoomNumber, RoomName, Heat)

        Lable = ["", "", "", "", ""]
        if data_rl[i]['utag']:
            for k in range(len(data_rl[i]['utag'])):
                Lable[k] = data_rl[i]['utag'][k]['name']
        print(Lable[0],Lable[1],Lable[2],Lable[3],Lable[4])

        Face = data_rl[i]['av']
        Face = 'https://apic.douyucdn.cn/upload/' + Face +'_big.jpg'#获取主播头像地址
        print("主播头像地址："+Face)
        # Face = ''

        detail_res = requests.get(detail_url+str(RoomNumber))
        detail_j = json.loads(detail_res.text)

        room_detail = detail_j['room']
        room_pic = str(room_detail['room_pic'])#获取直播间最新截图地址
        print("直播间最新截图地址：" + room_pic)

        html = (getHtmlurl(room_url+str(RoomNumber)))
        soup = BeautifulSoup(html, 'html.parser')

        levelDiv=soup.find('div', 'AnchorLevel')
        level = str(levelDiv).split('-')[1]
        level = level.split('"')[0]
        print('等级：'+level)

        driver.get(room_url+str(RoomNumber))
        driver.implicitly_wait(20)


        while True:
            Rank = driver.find_element_by_class_name("WeekRankTitle-upDownBoxMiddleConRank")
            time.sleep(1)
            if Rank.text != "--":
                break
        print('排名：'+Rank.text)

        wait = WebDriverWait(driver, 10)
        span = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'Title-followNum')))

        span_style = span.get_attribute('style')
        span_text = span.text

        font_url = str(span_style).split("douyu")[1]
        font_url = font_url.split(';')[0]

        first_url = "https://shark.douyucdn.cn/app/douyu/res/font/"

        r = requests.get(first_url + str(font_url) + ".woff")
        with open("demo.woff", "wb") as code:
            code.write(r.content)
        font = TTFont("demo.woff")
        font.saveXML('to.xml')

        # 打开xml文档
        dom = xml.dom.minidom.parse('to.xml')

        # 得到文档元素对象
        root = dom.documentElement


        GlyphOrder = root.getElementsByTagName('GlyphOrder')
        GlyphOrder_temp = GlyphOrder[0]

        GlyphIDlist = GlyphOrder_temp.getElementsByTagName("GlyphID")

        matrix = [0] * 10  # 存放对应关系 eg：matrix[8]=4 则8对应4
        # GlyphID = GlyphIDlist[0]
        for i in range(1, 11):
            if GlyphIDlist[i].getAttribute("name") == "one":
                matrix[1] = int(GlyphIDlist[i].getAttribute("id")) - 1
            if GlyphIDlist[i].getAttribute("name") == "two":
                matrix[2] = int(GlyphIDlist[i].getAttribute("id")) - 1
            if GlyphIDlist[i].getAttribute("name") == "three":
                matrix[3] = int(GlyphIDlist[i].getAttribute("id")) - 1
            if GlyphIDlist[i].getAttribute("name") == "four":
                matrix[4] = int(GlyphIDlist[i].getAttribute("id")) - 1
            if GlyphIDlist[i].getAttribute("name") == "five":
                matrix[5] = int(GlyphIDlist[i].getAttribute("id")) - 1
            if GlyphIDlist[i].getAttribute("name") == "six":
                matrix[6] = int(GlyphIDlist[i].getAttribute("id")) - 1
            if GlyphIDlist[i].getAttribute("name") == "seven":
                matrix[7] = int(GlyphIDlist[i].getAttribute("id")) - 1
            if GlyphIDlist[i].getAttribute("name") == "eight":
                matrix[8] = int(GlyphIDlist[i].getAttribute("id")) - 1
            if GlyphIDlist[i].getAttribute("name") == "nine":
                matrix[9] = int(GlyphIDlist[i].getAttribute("id")) - 1

        length = len(span_text)

        true_followNum = 0
        for k in range(0, length):
            true_followNum += matrix[int(span_text[k])] * pow(10, length - 1 - k)

        print(true_followNum)

        # 构造sql语句
        sql = '''insert into roomtable values(?,?,?,?,?,?,?,?,?,?)'''
        # 执行sql语句
        for t in [(RoomNumber,RoomName,str(Anchor),str(Lable),Heat,Face,room_pic,Rank.text,level,true_followNum)]:
            cursor.execute(sql, t)
        connect.commit()

# 关闭游标
cursor.close()
# 关闭数据库
connect.close()


driver.quit()


