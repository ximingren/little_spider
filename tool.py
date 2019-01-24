import datetime
import os
import threading
import time
import js2py
from lxml import etree
import requests
import pandas as pd
from selenium.webdriver.chrome import webdriver
from config import *

JS_PATH = './js/'
COOKIE_PATH = './cookie/'

class MyThread(threading.Thread):
    def __init__(self, func, args=None):
        super(MyThread, self).__init__()
        self.func = func

    def run(self):
        self.result = self.func()

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None


def get_proxy():
    """
    生成代理
    :return:
    """
    # 代理服务器
    proxyHost = "http-dyn.abuyun.com"
    proxyPort = "9020"
    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxyHost,
        "port": proxyPort,
        "user": proxyUser,
        "pass": proxyPass,
    }
    proxies = {
        "http": proxyMeta,
        "https": proxyMeta,
    }
    return proxies


def preprocess(data_list):
    """
    对数据进行预处理后再存入数据库中
    :param data_list: 数据列表
    :return:
    """
    pd.set_option('display.width', 2000)
    data = pd.DataFrame(data_list)
    result = []
    try:
        if not data.empty:
            for i in data.groupby(
                    ['room_id', 'start_time', 'breakfast_type', 'bed_type','crawl_time','hotel_name']).groups.values():
                if '在线付' not in data.iloc[i]['pay_type']:
                    sorted_data=data.iloc[i].sort_values(by='price')
                    result.append(sorted_data.iloc[0])
    except Exception as e:
        exit(1)
    finally:
        return result


def get_oceanball():
    """
    得到随机的oceanball的js文件
    :return:
     oceanball: oceanball随机js文件的url
     cas: 产生eleven的随机函数
    """
    oceanball = 'http://hotels.ctrip.com/domestic/cas/oceanball?callback=%s&_=%s'
    f = open(JS_PATH + 'get_callback.js')
    callback_js = f.read()
    ctxt = js2py.EvalJs()
    ctxt.eval('var callback = %s' % callback_js)
    ctxt.eval('cas = callback(15)')
    ctxt.eval('var current_time = (new Date).getTime()')
    cas = ctxt.cas
    current_time = ctxt.current_time
    oceanball = oceanball % (cas, int(current_time))
    return (oceanball, cas)


def get_eleven(hotel_id):
    """
    从oceanball中得到eleven
    :return: eleven(得到酒店信息必备的一个参数)
    """
    oceanball, cas = get_oceanball()
    headers = {
                'Accept': "*/*",
            'Accept-Encoding': "gzip, deflate",
            'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8",
            'Cache-Control': "no-cache",
            'Connection': "keep-alive",
            'Content-Type': "application/x-www-form-urlencoded; charset=utf-8",
            'Host': "hotels.ctrip.com",
            'If-Modified-Since': "Thu, 01 Jan 1970 00:00:00 GMT",
            'Referer': "http://hotels.ctrip.com/domestic/hotel/%s.html?isFull=F"%hotel_id,
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",
            'Postman-Token': "3aa8586c-caee-45a7-8cfd-5d2cbee1df43",
        }
    ocean =openlink(oceanball,type=2,headers=headers)
    ocean = ocean.replace('eval', 'JSON.stringify')
    ctxt = js2py.EvalJs()
    ocean = ctxt.eval(ocean)
    ocean = eval(ocean)
    ocean = ocean.replace(cas, 'eleven=' + cas)
    ctxt.eval('var hotel_id="%s";'%hotel_id)
    ctxt.eval(
        """var document = {URL: "http://hotels.ctrip.com/domestic/hotel/"+hotel_id+".html?isFull=F",baseURI: "http://hotels.ctrip.com/domestic/hotel/"+hotel_id+".html?isFull=F",body: {innerHTML: 333},createElement: function () {return new Foo();},documentElement: {attributes:{webdriver:{}}},documentURI: "http://hotels.ctrip.com/domestic/hotel/"+hotel_id+".html?isFull=F",domain: "hotels.ctrip.com",host: "hotels.ctrip.com",hostname: "hotels.ctrip.com",href: "http://hotels.ctrip.com/domestic/hotel/"+hotel_id+".html?isFull=F",origin: "http://hotels.ctrip.com"};""")
    ctxt.eval("""var html = {innerHTML: '1234', attributes: {webdriver: {}}};function Foo(){};var foo=new Foo();""")
    ctxt.eval('var %s = function(x){return x()};' % cas)
    ctxt.eval(
        """var window = {document: {},navigator: {appCodeName: "Mozilla", appName: "Netscape", language: "zh-CN", platform: "Win"},location: {href:"http://hotels.ctrip.com/domestic/hotel/"+hotel_id+".html?isFull=F"},HTMLSpanElement:Foo};""")
    ctxt.eval("""var div = {innerHTML: "333"};""")
    ctxt.eval("""var Image = function () {};""")
    ctxt.eval("""var eval=function(){function toString(){ return 1;}};""")
    ctxt.eval(
        """var navigator = {userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36", appCodeName: "Mozilla", appName: "Netscape", language: "zh", geolocation: function () {},};""")
    ctxt.eval("""var location = {href: "http://hotels.ctrip.com/domestic/hotel/"+hotel_id+".html?isFull=F"};""")
    ctxt.eval(ocean)
    eleven = ctxt.eleven
    return eleven



def openlink(url, type=None, headers=None, data=None, params=None):
    """
    连接
    :param url:
    :param type:
    :param headers:
    :param data:
    :param params:
    :return:
    """
    while True:
        try:
            proxy = get_proxy()
            response=None
            if use==1:
                response = requests.get(url, headers=headers, data=data, params=params,proxies=proxy)
            else:
                response = requests.get(url, headers=headers, data=data, params=params)
            if response.status_code == 407:
                print('请输入正确的代理通道')
                exit(1)
            if response.status_code == 402:
                print('请续费代理通道')
                time.sleep(15)
                exit(1)
            if '验证访问' in response.text:
                raise Exception
            if response.status_code == 200:
                if type == 0:
                    return response.json()
                elif type == 2:
                    ocean=response.text
                    ocean = ocean.replace('eval', 'JSON.stringify')
                    ctxt = js2py.EvalJs()
                    ocean = ctxt.eval(ocean)
                    return response.text
                else:
                    
                    return etree.HTML(response.text).xpath('string(//div[@class="path_bar2"]/h1)'),etree.HTML(response.text).xpath('string(//input[@id="cityId"]/@value)')
        except Exception as e:
            print('被反爬了',str(e))


def runTask(func, day=0, hour=0, min=0, second=0):
    """
    定时任务
    :param func:
    :param day:
    :param hour:
    :param min:
    :param second:
    :return:
    """
    now = datetime.datetime.now()
    period = datetime.timedelta(days=day, hours=hour, minutes=min, seconds=second)
    strnext_time = now.strftime('%Y-%m-%d %H:%M:%S')
    print(strnext_time+" "+"开始爬取")
    func()
    end_time=datetime.datetime.now()
    print(end_time.strftime('%Y-%m-%d %H:%M:%S')+" "+"爬取完成")
    strnext_time=(end_time+period).strftime('%Y-%m-%d %H:%M:%S')
    if end_time.hour>=7 and end_time.hour<=20:
        print('下一个爬取时间为'+' '+strnext_time)
    elif end_time.hour<=24 and end_time.hour>=20:
        print('下一个爬取时间为'+' '+str((end_time+datetime.timedelta(days=1)).date()+" 07:00:00"))
    else:
        print('下一个爬取时间为'+' '+str(end_time.date())+" 07:00:00")
    while True:
        iter_now = datetime.datetime.now()
        iter_now_time = iter_now.strftime('%Y-%m-%d %H:%M:%S')
        if iter_now.hour>=7 and iter_now.hour<=22:
            if str(iter_now_time) == str(strnext_time):
                print(str(iter_now_time)+" "+"开始爬取")
                func()
                end_time=datetime.datetime.now()
                print(end_time.strftime('%Y-%m-%d %H:%M:%S')+" "+"爬取完成")
                iter_time = end_time + period
                strnext_time = iter_time.strftime('%Y-%m-%d %H:%M:%S')
                print('下一个爬取时间为'+' '+strnext_time)
        else:
            strnext_time=str(iter_now.date())+" 07:00:00"

def gen_ctrip_ticket(self, update_freq):
    '''
    Use selenium to generate ticket cookie. The ticket will be saved in COOKIE_PATH
    Parameters
    ----------
    update_freq: int
        frequency of updating ticket (in seconds)
    '''
    while 1:
        try:
            if not os.path.exists(COOKIE_PATH + 'ticket.csv'):  # If not exist, make file
                ticketdf = pd.DataFrame({'ticket': ['Null']})
                ticketdf.to_csv(COOKIE_PATH + 'ticket.csv', index=False)
            driver = webdriver.Chrome('E:\ctrip_spider-master\chromedriver.exe')
            driver.set_page_load_timeout(10)
            button = '//*[@id="J_RoomListTbl"]/tbody/tr[3]/td[9]/div/a/div[1]'
            url1 = 'http://hotels.ctrip.com/Domestic/ShowHotelInformation.aspx?hotel=433176'
            driver.get(url1)
            driver.find_element_by_xpath(button).click()
            time.sleep(5)
            for i in driver.get_cookies():
                print(i['name'] + '  ' + i['value'])
            ticket = driver.get_cookie('ticket_ctrip')['value']
            print(ticket)
            if ticket != None:
                ticketdf = pd.DataFrame({'ticket': [ticket]})
                ticketdf.to_csv(COOKIE_PATH + 'ticket.csv', index=False)
                time.sleep(update_freq)  # update cookie after update_freq time
            driver.close()
        except Exception as e:
            print(e)
            # driver.close()
            ticketdf = pd.DataFrame({'ticket': ['Null']})
            ticketdf.to_csv(COOKIE_PATH + 'ticket.csv', index=False)
