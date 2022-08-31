import js2py
import requests
import execjs
import logging
from loguru import logger
import time

logging.captureWarnings(True)

bpproxy={
  "http": "http://127.0.0.1:8080",
  "https": "http://127.0.0.1:8080",
}

def get_blob(plainText, AES_KEY, AES_IV):
    with open("./enc.js", "r") as f:
        data_func = f.read()        #读取js文件
    tk = execjs.compile(data_func,cwd=r"./node_modules")  # 编译执行js代码
    tk = tk.call('aes_encrypt',plainText, AES_KEY, AES_IV)        # 调用函数 token为js里面的函数  a为传的参数
    tk = str(tk)
    return tk

def get_oraw(e_date,e_time):
    js_code = '''
          var date = new Date().getTime()   
    '''
    e_timemill=js2py.eval_js(js_code)
    raw=f'{{"date":"{e_date}","time":"{e_time}","timemill":{e_timemill}}}'
    oraw=''
    for i in range(len(raw)):
        tmp=raw[i]+raw[len(raw)-1-i]
        oraw+=tmp
    return oraw

def order(mycookie,ekey,date,time):
    oraw = get_oraw(date, time)
    blob = get_blob(oraw, ekey[0:16], ekey[2:18])
    url='https://gym.byr.moe'
    r=requests.session()
    result=r.post(url+'/newOrder.php',data={'blob':blob},verify=False,cookies=mycookie,proxies=bpproxy).text
    if result=='1':
        logger.info('预约成功!')
    elif result=='2':
        logger.info('非法请求!')
    elif result=='3':
        logger.info('本时间段人数已满!')
    elif result=='4':
        logger.info('您已预约本时段健身房!')
    elif result=='5':
        logger.info('参数错误！')
    else:
        logger.info('未知错误类型！'+result)

def intruder(level,cookie,ekey,date,ttime):
    while True:
        order(cookie,ekey,date,ttime)
        time.sleep(level)

if __name__ == "__main__":
    print('请输入你的PHPsession：')
    sess=input()
    print('请输入你的学号：')
    ekey=input()
    ekey += ekey
    print('请输入想预约的日期（格式20021130）：')
    e_date=input()
    print('''请输入想预约的时间段（1或2或3）：
        1. 18:40 - 19:40
        2. 19:40 - 20:40
        3. 20:40 - 21:40''')
    e_time=input()
    cookie={'PHPSESSID':sess}
    intruder(1.8, cookie, ekey, e_date, e_time)

