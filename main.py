import requests
import os
import sys

# 从 GitHub Secrets 中读取
BARK_KEY = os.getenv("BARK_KEY")
WEATHER_KEY = os.getenv("WEATHER_KEY")
TIAN_KEY = os.getenv("TIAN_KEY")

def get_data():
    # 1. 天气诊断
    weather_info = "天气获取失败"
    try:
        w_url = f"https://devapi.qweather.com/v7/weather/now?location=101010100&key={WEATHER_KEY}"
        res = requests.get(w_url)
        print(f"DEBUG: 天气接口状态码: {res.status_code}")
        # 如果返回的是加密或错误页面，这里能看到原因
        data = res.json()
        if data.get('code') == '200':
            w = data['now']
            weather_info = f"天气：{w['text']}，{w['temp']}°C"
        else:
            weather_info = f"天气报错代码: {data.get('code')}"
            print(f"DEBUG: 天气完整返回: {data}")
    except Exception as e:
        weather_info = f"天气解析异常"
        print(f"DEBUG: 天气异常信息: {e}")

    # 2. 星座诊断
    star_info = "运势获取失败"
    try:
        s_url = f"https://apis.tianapi.com/star/index?key={TIAN_KEY}&astro=lion"
        res = requests.get(s_url)
        data = res.json()
        if data.get('code') == 200:
            star_info = data['result'].get('content', '暂无内容')
        else:
            star_info = f"运势报错: {data.get('msg')}"
            print(f"DEBUG: 星座完整返回: {data}")
    except Exception as e:
        star_info = "运势解析异常"
        print(f"DEBUG: 星座异常信息: {e}")

    return weather_info, star_info

if __name__ == "__main__":
    w, s = get_data()
    msg = f"{w}\n\n运势：{s}"
    # 推送到手机
    push_url = f"https://api.day.app/{BARK_KEY}/早安校准/{msg}"
    requests.get(push_url)
    print("DONE: 推送请求已发出")
