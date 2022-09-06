from datetime import date, datetime, timedelta
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
import json

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)



nowtime = datetime.utcnow() + timedelta(hours=8)  # 东八区时间
today = datetime.strptime(str(nowtime.date()), "%Y-%m-%d") #今天的日期

start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY_JING']
birthday1 = os.environ['BIRTHDAY_XUAN']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
user_id_1 = os.environ["USER_ID_1"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp']), weather['airQuality'], math.floor(weather['low']), math.floor(weather['high'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_birthday1():
  next = datetime.strptime(str(date.today().year) + "-" + birthday1, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days


def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_cov_data():
  url = "http://api.tianapi.com/ncov/index?key=0a764a755797c95e01cad9af5c0dfc29"
  res = requests.get(url).json()
  cov_data = res['newslist'][0]['news'][0]['summary']
  return cov_data

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature, airQuality, low_temp, high_temp= get_weather()
data = {"city":{"value":city, "color":get_random_color()},
        "date":{"value":today.strftime('%Y年%m月%d日'), "color":get_random_color()},
        "weather":{"value":wea, "color":get_random_color()},
        "temperature":{"value":temperature, "color":get_random_color()},
        "airQuality":{"value":airQuality, "color":get_random_color()},
        "min_temperature":{"value":low_temp, "color":get_random_color()},
        "max_temperature":{"value":high_temp, "color":get_random_color()},
        "love_days":{"value":get_count(), "color":get_random_color()},
        "birthday_left":{"value":get_birthday(), "color":get_random_color()},
        "birthday_left1":{"value":get_birthday1(), "color":get_random_color()},
        "words":{"value":get_words(), "color":get_random_color()},
        "cov_data":{"value":get_cov_data(), "color":get_random_color()}}

# data = json.dumps(data,cls=ComplexEncoder)
res = wm.send_template(user_id, template_id, data)
res_1 = wm.send_template(user_id_1, template_id, data)
print(res)
