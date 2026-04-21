import requests
import os
import sys

# 从 GitHub Secrets 中读取
BARK_KEY = os.getenv("BARK_KEY")
WEATHER_KEY = os.getenv("WEATHER_KEY")
TIAN_KEY = os.getenv("TIAN_KEY")

def get_data():
    # 1. 天气 (和风) - 换成 location=beijing 试试，确保 Key 是 Web API 类型
    weather_info = "天气获取失败"
    try:
        # 注意：这里我们换成了城市拼音，增加兼容性
        w_url = f"https://devapi.qweather.com/v7/weather/now?location=101010100&key={WEATHER_KEY.strip()}"
        res = requests.get(w_url)
        data = res.json()
        if data.get('code') == '200':
            w = data['now']
            weather_info = f"天气：{w['text']}，{w['temp']}°C"
        else:
            weather_info = f"天气Key或权限问题({data.get('code')})"
    except:
        weather_info = "天气解析异常"

    # 2. 星座 (天行) - 换成中文星座名
    star_info = "运势获取失败"
    try:
        # 天行数据有时对中文星座名支持更好
        s_url = f"https://apis.tianapi.com/star/index?key={TIAN_KEY.strip()}&astro=狮子座"
        res = requests.get(s_url)
        data = res.json()
        if data.get('code') == 200:
            star_info = data['result'].get('content', '今日暂无运势更新')
        else:
            star_info = f"运势问题:{data.get('msg')}"
    except:
        star_info = "运势解析异常"

    return weather_info, star_info

if __name__ == "__main__":
    w, s = get_data()
    msg = f"{w}\n\n运势：{s}"
    # 推送到手机
    push_url = f"https://api.day.app/{BARK_KEY}/早安校准/{msg}"
    requests.get(push_url)
    print("DONE: 推送请求已发出")
