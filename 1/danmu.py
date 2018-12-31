'''
利用斗鱼弹幕 api
尝试抓取斗鱼tv指定房间的弹幕
'''

import multiprocessing
import socket
import time
import re
import signal
import sqlite3
import threading

#连接到数据库
connect = sqlite3.connect("zhubo.sqlite3")
# 创建了一个游标对象：cursor
cursor = connect.cursor()

rooms = []#存储房间列表
sql = '''select room_id from roomtable order by hot desc'''
cursor.execute(sql)    #该例程执行一个 SQL 语句
rooms=cursor.fetchall()      #该例程获取查询结果集中所有（剩余）的行，返回一个列表
room_s =[]
for r in rooms:
    r = str(r).split("('")[1]
    r = r.split("',")[0]
    print(r)
    room_s.append(r)
flag = 0

content_num=100

# 构造socket连接，和斗鱼api服务器相连接
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostbyname("openbarrage.douyutv.com")
port = 8601
client.connect((host, port))

# 弹幕查询正则表达式
danmu_re = re.compile(b'txt@=(.+?)/cid@')
username_re = re.compile(b'nn@=(.+?)/txt@')
userlevel_re = re.compile(b'level@=(.+?)/sahf@')


def send_req_msg(msgstr):
    '''构造并发送符合斗鱼api的请求'''

    msg = msgstr.encode('utf-8')
    data_length = len(msg) + 8
    code = 689
    # 构造协议头
    msgHead = int.to_bytes(data_length, 4, 'little') \
              + int.to_bytes(data_length, 4, 'little') + \
              int.to_bytes(code, 4, 'little')
    client.send(msgHead)
    sent = 0
    while sent < len(msg):
        tn = client.send(msg[sent:])
        sent = sent + tn


def DM_start(rid):
    # 构造登录授权请求
    msg = 'type@=loginreq/roomid@={}/\0'.format(rid)
    send_req_msg(msg)
    # 构造获取弹幕消息请求
    msg_more = 'type@=joingroup/rid@={}/gid@=-9999/\0'.format(rid)
    send_req_msg(msg_more)

    while True:
        # 服务端返回的数据
        data = client.recv(1024)
        # 通过re模块找发送弹幕的用户名和内容
        danmu_username = username_re.findall(data)
        danmu_userlevel = userlevel_re.findall(data)
        danmu_content = danmu_re.findall(data)

        if not data:
            break
        # else:
        #     for i in range(0, len(danmu_content)):
        #         try:
        #             # 输出信息
        #             print('[{}({})]:{}'.format(danmu_username[0].decode('utf8'), danmu_userlevel[0].decode('utf8'),
        #                                        danmu_content[0].decode(encoding='utf8')))
        #         except:
        #             continue
        else:
            for i in range(content_num):
                try:



def keeplive():
    '''
    保持心跳，15秒心跳请求一次
     '''
    while True:
        msg = 'type@=keeplive/tick@=' + str(int(time.time())) + '/\0'
        send_req_msg(msg)
        print('发送心跳包')
        time.sleep(15)


def logout():
    '''
    与斗鱼服务器断开连接
    关闭线程
    '''
    msg = 'type@=logout/'
    send_req_msg(msg)
    print('已经退出服务器')


def signal_handler(signal, frame):
    '''
    捕捉 ctrl+c的信号 即 signal.SIGINT
    触发hander：
    登出斗鱼服务器
    关闭进程
    '''
    p1.terminate()
    p2.terminate()
    logout()
    print('Bye')

# 获取文件中的房间号
# f = open("danmu.txt", mode='r')
# line = f.readlines()
# roomid = [i.strip() for i in line]
# f.close()
#
# islive = False
# thread_num = 4

#     # 创建线程
#     threads = []
#     for room_id in roomid:
#         print("房间号" + room_id)
#         try:
#             if len(threads) >= thread_num:
#                 islive = True
#                 while islive and len(threads) >= thread_num:
#                     for i in range(len(threads)):
#                         islive = islive and threads[i].isAlive()
#                     if (islive):
#                         time.sleep(5)
#                     for i in range(len(threads)):
#                         if not threads[i].isAlive():
#                             del threads[i]
#                             break
#
#             t = threading.Thread(target=DM_start, args=(room_id,))
#             threads.append(t)
#             t.start()
#             time.sleep(15)
#
#         except:
#             print("线程创建失败")
#     for thread in threads:
#         thread.join(60)

if __name__ == '__main__':
    for room_id in room_s:
        # 开启弹幕和心跳进程
        p1 = multiprocessing.Process(target=DM_start, args=(room_id,))
        p2 = multiprocessing.Process(target=keeplive)
        p1.start()
        p2.start()

    # 开启signal捕捉
    signal.signal(signal.SIGINT, signal_handler)
