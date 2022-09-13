import js2py
import requests
import execjs
import logging
from loguru import logger
import time
import threading

logging.captureWarnings(True)

bpproxy = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080",
}


def get_blob(plainText, AES_KEY, AES_IV):
    with open("./enc.js", "r") as f:
        data_func = f.read()
    ex = execjs.compile(data_func, cwd=r"./node_modules")
    ex = ex.call('aes_encrypt', plainText, AES_KEY, AES_IV)
    ex = str(ex)
    return ex


def get_oraw(e_date, e_time):
    js_code = '''
          var date = new Date().getTime()   
    '''
    e_timemill = js2py.eval_js(js_code)
    raw = f'{{"date":"{e_date}","time":"{e_time}","timemill":{e_timemill}}}'
    oraw = ''
    for i in range(len(raw)):
        tmp = raw[i] + raw[len(raw) - 1 - i]
        oraw += tmp
    return oraw


def order(mycookie, ekey, date, time):
    oraw = get_oraw(date, time)
    blob = get_blob(oraw, ekey[0:16], ekey[2:18])
    url = 'https://gym.byr.moe'
    r = requests.session()
    result = r.post(url + '/newOrder.php', data={'blob': blob}, verify=False, cookies=mycookie, timeout=1).text
    if result == '1':
        logger.info(date[4:8] + '-' + time + ' 预约成功!')
        return result
    elif result == '2':
        logger.info(date[4:8] + '-' + time + ' 非法请求! (未到预约时间)')
        return result
    elif result == '3':
        logger.info(date[4:8] + '-' + time + ' 本时间段人数已满!')
        return result
    elif result == '4':
        logger.info(date[4:8] + '-' + time + ' 您已预约本时段健身房!')
        return result
    elif result == '5':
        logger.info(date[4:8] + '-' + time + ' 参数错误！')
        return result
    else:
        logger.info(date[4:8] + '-' + time + ' 未知错误类型！' + result)
        return result


def intruder(level, cookie, ekey, date, ttime):
    while True:
        result = order(cookie, ekey, date, ttime)
        time.sleep(level)
        if result == '1':
            return 'success'


if __name__ == "__main__":
    print('请输入你的PHPsession：')
    sess=input()
    print('请输入你的学号：')
    ekey=input()
    # ekey = '20202'
    ekey += ekey
    print('请输入想预约的日期（格式20021130）：')
    e_date = input()
    # print('''请输入想预约的时间段（1或2或3）：
    #     1. 18:40 - 19:40
    #     2. 19:40 - 20:40
    #     3. 20:40 - 21:40''')
    # e_time=input()
    cookie = {'PHPSESSID': sess}
    intruder(level=0.8, cookie=cookie, ekey=ekey, date=e_date, ttime='2')
    intruder(level=0.8, cookie=cookie, ekey=ekey, date=e_date, ttime='1')
    intruder(level=0.8, cookie=cookie, ekey=ekey, date=e_date, ttime='3')
