# -- coding: utf-8 --**
import json
import os
from hashlib import md5
import requests
import datetime #时间包
import random #随机
from requests.adapters import HTTPAdapter
import linecache #文件读写
from urllib3.connectionpool import xrange#xrange
import time #时间包、用于延时执行任务
import MessagePush

requests.adapters.DEFAULT_RETRIES = 10
pwd = os.path.dirname(os.path.abspath(__file__)) + os.sep

s = requests.session()
s.mount('http://', HTTPAdapter(max_retries=10))
s.mount('https://', HTTPAdapter(max_retries=10))
s.keep_alive = False

#获取今天的日期函数
currentDateAndTime = datetime.datetime.now() #获取日期、
day = currentDateAndTime.strftime("%Y-%m-%d")#格式化日期保存至day,今天的日期
end_time = currentDateAndTime.strftime("%Y-%m-%d")#结束日期的格式

def timej1(): #时间算法
    today = datetime.datetime.now()  # 获取今天日期
    #today1 = today.strftime("%Y-%m-%d")  # 格式化日期保存  ///%H:%M:%S时分秒
    aWeek = today - datetime.timedelta(days=6) #一周的算法
    format_aWeek = aWeek.strftime("%Y-%m-%d")
    return format_aWeek
begin_time = timej1() #算法处理过后的周报开始日期




#随机读写的配置
#num1是第一个随机数、num2是第二个随机数
#content1是生成的第一篇文、content2是第二篇
#tileContent1是最终传参第一篇 tileContent2是第二篇
for i in xrange(1):
    num1 = random.randrange(1, 29)
    content1 = linecache.getline(r'cookie.txt', num1)
    tileContent1 = content1.replace('\n', '').replace('\r', '')
for i in xrange(1):
    num2 = random.randrange(1, 29)
    content2 = linecache.getline(r'cookie.txt', num2)
    tileContent2 = content2.replace('\n', '').replace('\r', '')
#周报随机
for i in xrange(1):
    nums1 = random.randrange(1, 29)
    contents1 = linecache.getline(r'cookie.txt', nums1)
    tileContents1 = contents1.replace('\n', '').replace('\r', '')
for i in xrange(1):
    nums2 = random.randrange(1, 29)
    contents2 = linecache.getline(r'cookie.txt', nums2)
    tileContents2 = contents2.replace('\n', '').replace('\r', '')
headers = { #请求头参数
    "os": "android",#安卓
    "phone": "Xiaomi|Mi 12|12",#手机型号
    "appVersion": "39",#版本
    "Sign": "Sign",#sign验证
    "cl_ip": "192.168.1.2",#本地ip
    "User-Agent": "okhttp/3.14.9",
    "Content-Type": "application/json;charset=utf-8"

}

def getMd5(text: str): #获取 MD5
    return md5(text.encode('utf-8')).hexdigest()

def parseUserInfo():#窗口主程序
    allUser = ''
    if os.path.exists(pwd + "user.json"):
        print('找到配置文件，将从配置文件加载信息！')
        with open(pwd + "user.json", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                allUser = allUser + line + '\n'

    else:
        return json.loads(os.environ.get("USERS", ""))
    return json.loads(allUser)


def getToken(): #获取Token
    url = 'http://sxbaapp.zcj.jyt.henan.gov.cn/interface/token.ashx'
    res = requests.post(url, headers=headers)
    if res.json()["code"] == 1001:
        return True, res.json()["data"]["token"]
    return False, res.json()["msg"]


def login(user, token): #登录
    password = getMd5(user["password"]) #获取密码的md5赋值给密码
    deviceId = user["deviceId"] #这个id无所谓但要有

    data = {
        "phone": user["phone"], #账号=手机号
        "password": password, #密码
        "dtype": 6,
        "dToken": deviceId #无所谓的东西
    }
    headers["Sign"] = getMd5((json.dumps(data) + token))
    url = 'http://sxbaapp.zcj.jyt.henan.gov.cn/interface/relog.ashx'
    res = requests.post(url, headers=headers, data=json.dumps(data))
    return res.json()




def dayBao(uid, token, day, tileContent1, tileContent2): #日报
    url = 'http://sxbaapp.zcj.jyt.henan.gov.cn/interface/ReportHandler.ashx'

    data = {
        "uid": uid,#传入UID
        "starttime": day,#传入今天的day
        "project": "保密",
        "address": "公司",
        "record": tileContent1,
        "summary": tileContent2,
        "dtype": 1
    }
    headers["Sign"] = getMd5((json.dumps(data) + token))
    res = requests.post(url, headers=headers, data=json.dumps(data))

    if res.json()["code"] != 1001:
        MessagePush.pushMessage('日报没写上请你检查一下吧', '用户：' + user["phone"] + '\n你的日报没有写上，请你检查代码看哪里有错误', user["pushKey"])
        print('日报可没有弄上去啊，检查代码吧')
        return
    MessagePush.pushMessage('日报写完了', '用户：' + user["phone"] + '\n' + tileContent1 + '\n' + '\n' + tileContent2, user["pushKey"])
    print('日报写完啦')
    return res.json()


def weekBao(uid, token, day, tileContents1, tileContents2, begin_time, end_time):#周报
    url = 'http://sxbaapp.zcj.jyt.henan.gov.cn/interface/ReportHandler.ashx'

    data = {
        "uid": uid,  # 传入UID
        "starttime": begin_time,  # 周开始时间，通常填写周一,开始的时间
        "project": "保密",
        "address": "公司",
        "record": tileContents1,
        "summary": tileContents2,
        "dtype": 2,
        "stype": 2,
        "endtime": end_time #周结束时间，通常填写周日,结束的时间
    }
    headers["Sign"] = getMd5((json.dumps(data) + token))
    res = requests.post(url, headers=headers, data=json.dumps(data))

    if res.json()["code"] != 1001:
        MessagePush.pushMessage('周报没写上请你检查一下吧', '用户：' + user["phone"] + '\n请你检查代码看哪里有错误', user["pushKey"])
        print('日报可没有弄上去啊，检查代码吧')
        return
    MessagePush.pushMessage('周报可是写了', '用户：' + user["phone"] + '\n' + tileContents1 + '\n' + '\n' + tileContents2 + '\n' + '\n' + '\n' + '开始时间:' + begin_time + '\n' + '结束时间:' + end_time, user["pushKey"])
    print('周报写完啦')
    return res.json()


def monthBao(uid, token):
    url = 'http://sxbaapp.zcj.jyt.henan.gov.cn/interface/ReportHandler.ashx'

    data = {
        "uid": uid,  # 传入UID
        "starttime": "2022-12-01",  # 月开始时间，通常填写一号
        "project": "保密",
        "address": "保密",
        "record": "实习我真爱我真爱实习我真爱实习我太爱你阿实习",
        "summary": "天天要实习",
        "dtype": 2,
        "stype": 3,
        "endtime": "2022-12-31"  # 月结束时间，通常填写月底
    }
    headers["Sign"] = getMd5((json.dumps(data) + token))
    res = requests.post(url, headers=headers, data=json.dumps(data))
    return res.json()


def save(user, uid, token): #打卡
    url = 'http://sxbaapp.zcj.jyt.henan.gov.cn/interface/clockindaily20220827.ashx'

    data = {
        "dtype": 1,
        "uid": uid, #UID
        "address": user["address"], #地址
        "phonetype": user["deviceType"], #手机型号
        "probability": -1,
        "longitude": user["longitude"],#经度
        "latitude": user["latitude"] #维度
    }
    headers["Sign"] = getMd5(json.dumps(data) + token)
    res = requests.post(url, headers=headers, data=json.dumps(data))

    if res.json()["code"] == 1001:
        return True, res.json()["msg"]
    return False, res.json()["msg"]

def prepareSign(user):
    if not user["enable"]:
        print(user['alias'], '未启用打卡，即将跳过')
        return

    print('已加载用户', user['alias'], '登录成功')
    headers["phone"] = user["deviceType"]

    res, token = getToken() #获取Token

    if not res:
        print('用户', user['alias'], '获取Token失败')
        return

    loginResp = login(user, token) #运行登录
    uid = loginResp["data"]["uid"] #uid 获取

    if loginResp["code"] != 1001:
        print('用户', user['alias'], '登录账号失败，错误原因：', loginResp["msg"])
        return

    #weekBao(uid,token)#周报
    #monthBao(uid,token)#月报

    resp, msg = save(user, uid, token)#打卡
    time.sleep(60)  # 延时60秒执行打卡日报
    dayBao(uid, token, day, tileContent1, tileContent2)  # 日报运行

    # 判断打卡条件，day是日期的判断
    if day == '2022-12-25' or day == '2023-01-01' or day == '2023-01-08' or day == '2023-01-15' or day == '2023-01-22' or day == '2023-01-29' or day == '2023-02-05' or day == '2023-02-12' or day == '2023-02-19' or day == '2023-02-26' or day == '2023-03-05' or day == '2023-03-12' or day == '2023-03-19' or day == '2023-03-26' or day == '2023-04-02':
        weekBao(uid, token, day, tileContents1, tileContents1, begin_time, end_time)
        #里面写的都是周报的日期
    else:
        print('今天不是写周报的时间')

    ##打卡推送信息
    if resp:
        print(user["alias"], '打卡成功！')
        MessagePush.pushMessage('职校家园打卡成功！', '用户：' + user["phone"] + '职校家园打卡成功!', user["pushKey"])
        return
    print(user["alias"], "打卡失败")

    MessagePush.pushMessage('职校家园打卡失败！', '用户：' + user["phone"] + '职校家园打卡失败!原因:' + msg, user["pushKey"])

if __name__ == '__main__':
    users = parseUserInfo()

    for user in users:
        try:
            prepareSign(user)
        except Exception as e:
            print('职校家园打卡失败，错误原因：' + str(e))
            MessagePush.pushMessage('职校家园打卡失败',
                                    '职校家园打卡失败,' +
                                    '具体错误信息：' + str(e)
                                    , user["pushKey"])
