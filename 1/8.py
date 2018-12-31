import requests
from fontTools.ttLib import TTFont
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import  xml.dom.minidom



chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument('headless')
chromeOptions.add_argument('window-size=1200x600')

driver = webdriver.Chrome()


driver.get("https://www.douyu.com/208114")
driver.set_window_size(1024, 768)

wait = WebDriverWait(driver, 10)
span = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'Title-followNum')))


#span = driver.find_element_by_class_name("Title-followNum")
span_style = span.get_attribute('style')
span_text = span.text
print(span_text)
print(span_style)

url = str(span_style).split("douyu")[1]
url = url.split(';')[0]

print(url)
first_url = "https://shark.douyucdn.cn/app/douyu/res/font/"

r = requests.get(first_url+str(url)+".woff")
with open("demo.woff", "wb") as code:
    code.write(r.content)
font = TTFont("demo.woff")
font.saveXML('to.xml')

driver.quit()

#打开xml文档
dom = xml.dom.minidom.parse('to.xml')

#得到文档元素对象
root = dom.documentElement
print (root.nodeName)

GlyphOrder = root.getElementsByTagName('GlyphOrder')
GlyphOrder_temp = GlyphOrder[0]

GlyphIDlist = GlyphOrder_temp.getElementsByTagName("GlyphID")

matrix=[0]*10 # 存放对应关系 eg：matrix[8]=4 则8对应4
#GlyphID = GlyphIDlist[0]
for i in range(1,11):
    print ("id:"+GlyphIDlist[i].getAttribute("id")+"    name:"+GlyphIDlist[i].getAttribute("name"))
    if GlyphIDlist[i].getAttribute("name")=="one" :
        matrix[1]=int(GlyphIDlist[i].getAttribute("id"))-1
    if GlyphIDlist[i].getAttribute("name")=="two" :
        matrix[2]=int(GlyphIDlist[i].getAttribute("id"))-1
    if GlyphIDlist[i].getAttribute("name")=="three" :
        matrix[3]=int(GlyphIDlist[i].getAttribute("id"))-1
    if GlyphIDlist[i].getAttribute("name")=="four" :
        matrix[4]=int(GlyphIDlist[i].getAttribute("id"))-1
    if GlyphIDlist[i].getAttribute("name")=="five" :
        matrix[5]=int(GlyphIDlist[i].getAttribute("id"))-1
    if GlyphIDlist[i].getAttribute("name")=="six" :
        matrix[6]=int(GlyphIDlist[i].getAttribute("id"))-1
    if GlyphIDlist[i].getAttribute("name")=="seven" :
        matrix[7]=int(GlyphIDlist[i].getAttribute("id"))-1
    if GlyphIDlist[i].getAttribute("name")=="eight" :
        matrix[8]=int(GlyphIDlist[i].getAttribute("id"))-1
    if GlyphIDlist[i].getAttribute("name")=="nine" :
        matrix[9]=int(GlyphIDlist[i].getAttribute("id"))-1

print(matrix)
length = len(span_text)
print(length)
true_followNum =0
for k in range(0,length):
    true_followNum += matrix[int(span_text[k])]*pow(10,length-1-k)
print(true_followNum)

